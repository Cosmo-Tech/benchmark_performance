"""Script create container in your account storage"""
from storage.create_container import create_container_upsert
if __name__ == '__main__':
    create_container_upsert("performance-datasets")
    create_container_upsert("performance-results")
