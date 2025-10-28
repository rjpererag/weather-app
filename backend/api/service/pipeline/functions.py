from uuid import UUID

from ..db_manager.models import TransactionsORM
from ..db_manager.definitions import Transaction
from ..db_manager.handlers import *
from ..utils import IDGenerator

def fetch_coordinates(db_url: str, payload: dict) -> dict:
	coordinates_handler = CoordinatesHandler(db_url=db_url)
	coordinates = coordinates_handler.get_coordinates(city_name=payload.get("city_name"))

	return {
		"city_name": coordinates.get("city_name"),
		"coordinates_id": str(coordinates.get("coordinates_id")),
		"latitude": coordinates.get("latitude"),
		"longitude": coordinates.get("longitude"),
	}

def generate_ids(payload: dict) -> dict:
	id_generator = IDGenerator(payload=payload)
	ids = id_generator.generate_ids()
	return {
		"base_id": ids.get("base_id"),
		"raw_layer_id": ids.get("raw_layer_id"),
		"results_id": ids.get("results_id"),
	}

def create_new_transaction(db_url: str, payload: dict) -> dict:
	transactions_orm = TransactionsORM(db_url=db_url)
	transaction = transactions_orm.create(payload=payload, status_id=0)

	# TODO: THIS MUST BE LOGS
	print(f"New transaction created, id to monitor = {transaction.id}")
	print(f"Monitoring transaction {transaction.id}")
	print(f"Status: {transaction.status_id}")

	return transaction.to_dict()


def get_transaction_by_id(db_url: str, id_: UUID | str) -> dict:
	transactions_orm = TransactionsORM(db_url=db_url)
	transaction = transactions_orm.get_by_id(t_id=id_)

	return transaction


def process_transaction(db_url: str, payload: dict) -> dict:
	# TODO: Chane to use logs
	print("Checking on Raw Layer Table")
	rl_handler = RawLayerHandler(db_url=db_url)
	raw_layer_record = rl_handler.monitor(payload=payload)
	payload["raw_layer"] = raw_layer_record

	# STEP 4 - Monitoring Processed layer
	print("Checking on Processed Layer Table")
	pl_handler = ProcessedLayerHandler(db_url=db_url)
	processed_layer_record = pl_handler.monitor(payload=payload)
	payload["processed_layer"] = processed_layer_record

	print(f"Results Available. Fetch results using: {processed_layer_record.id}")
	return payload


# TODO: MUST INCLUDE A FUNCTION TO UPDATE THE STATUS - WE MUST USE TRY - EXCEPT TO HANDLE ERROR
def get_results(db_url: str, payload: dict) -> dict:
	coordinates = fetch_coordinates(db_url=db_url, payload=payload)
	payload = {**payload, **coordinates}

	ids_generated = generate_ids(payload=payload)
	payload = {**payload, **ids_generated}

	transaction = create_new_transaction(db_url=db_url, payload=payload)
	payload = {**payload, **transaction}

	results = process_transaction(db_url=db_url, payload=payload)

	return results