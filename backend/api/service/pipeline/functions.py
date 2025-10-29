from uuid import UUID

from ..db_manager.models import TransactionsORM
from ..db_manager.models import ProcessedLayerORM
from ..db_manager.definitions import Transaction, ProcessedLayer
from ..db_manager.handlers import *
from ..utils import IDGenerator, logger

def fetch_coordinates(db_url: str, payload: dict) -> dict:
	logger.info(f"Getting coordinates for {payload.get('city_name')}")
	try:
		coordinates_handler = CoordinatesHandler(db_url=db_url)
		coordinates = coordinates_handler.get_coordinates(city_name=payload.get("city_name"))

		return {
			"city_name": coordinates.get("city_name"),
			"coordinates_id": str(coordinates.get("coordinates_id")),
			"latitude": coordinates.get("latitude"),
			"longitude": coordinates.get("longitude"),
		}
	except:
		logger.error(f"Failed getting coordinates for {payload.get('city_name')}")
		return {"error": f"coordinates not found"}

def generate_ids(payload: dict) -> dict:
	id_generator = IDGenerator(payload=payload)
	ids = id_generator.generate_ids()
	return {
		"base_id": ids.get("base_id"),
		"raw_layer_id": ids.get("raw_layer_id"),
		"results_id": ids.get("results_id"),
	}

def update_transaction_by_id(db_url: str, payload: dict, new_status_id: int) -> dict:
	# TODO: THIS MUST BE LOGS
	transaction_id = payload.get('id')

	print(f"Updating transaction = {transaction_id}")
	transactions_orm = TransactionsORM(db_url=db_url)
	transaction = transactions_orm.update_status_id(
		t_id=transaction_id,
		new_status_id=new_status_id,
	)
	print(f"Transaction Updated: {transaction_id}")
	print(f"New transaction status id: {transaction.status_id}")

	return transaction.to_dict()


def create_new_transaction(db_url: str, payload: dict) -> dict:
	try:
		transactions_orm = TransactionsORM(db_url=db_url)
		transaction = transactions_orm.create(payload=payload, status_id=0)

		# TODO: THIS MUST BE LOGS
		logger.info(f"	New transaction created, id to monitor = {transaction.id}")
		return transaction.to_dict()
	except:
		logger.error(f"	Failed creating new transaction")
		return {"error": "Failed creating new transaction"}


def get_transaction_by_id(db_url: str, id_: UUID | str) -> dict:
	transactions_orm = TransactionsORM(db_url=db_url)
	transaction = transactions_orm.get_by_id(t_id=id_)

	return transaction


def process_transaction(db_url: str, payload: dict) -> dict:
	try:
		logger.info("	Checking on Raw Layer Table")
		rl_handler = RawLayerHandler(db_url=db_url)
		raw_layer_record = rl_handler.monitor(payload=payload)
		payload["raw_layer"] = raw_layer_record.to_dict() if raw_layer_record else None

		logger.info("	Checking on Processed Layer Table")
		pl_handler = ProcessedLayerHandler(db_url=db_url)
		processed_layer_record = pl_handler.monitor(payload=payload)
		payload["processed_layer"] = processed_layer_record.to_dict() if processed_layer_record else None

		logger.info("	Monitoring finished")

		logger.info("	Updating transaction status")
		updated_transaction = update_transaction_by_id(
			db_url=db_url, payload=payload, new_status_id=1
		)

		logger.info(f"	Results Available. Fetch results using: {processed_layer_record.id}")

	except Exception as e:
		try:
			logger.error("	Failed processing transaction")
			updated_transaction = update_transaction_by_id(
				db_url=db_url, payload=payload, new_status_id=2
			)
			return {"error": "Failed processing transaction"}

		except:
			logger.error(f"	Failed updating failed transaction")
			return {"error": "Failed updating failed transaction"}

	return {**payload, **updated_transaction}

def get_results_by_id(db_url: str, pl_id: UUID | str) -> dict:
	orm = ProcessedLayerORM(db_url=db_url)
	results = orm.get_by_id(pl_id=pl_id)
	return results.to_dict()


# TODO: MUST INCLUDE A FUNCTION TO UPDATE THE STATUS - WE MUST USE TRY - EXCEPT TO HANDLE ERROR
def get_results(db_url: str, payload: dict):

	try:
		coordinates = fetch_coordinates(db_url=db_url, payload=payload)
		payload = {**payload, **coordinates}

		ids_generated = generate_ids(payload=payload)
		payload = {**payload, **ids_generated}

		transaction = create_new_transaction(db_url=db_url, payload=payload)
		payload = {**payload, **transaction}

		results = process_transaction(db_url=db_url, payload=payload)
		updated_transaction = update_transaction_by_id(
			db_url=db_url, payload=payload, new_status_id=1
		)

	except Exception as e:
		results = {"error": str(e)}
		updated_transaction = update_transaction_by_id(
			db_url=db_url, payload=payload, new_status_id=2
		)

	return results, updated_transaction