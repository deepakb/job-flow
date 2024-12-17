"""
Base repository interface and implementation.

This module provides the base repository pattern implementation for data access.
It defines common CRUD operations and database interaction patterns.
"""

from typing import Generic, TypeVar, Optional, List, Dict, Any
from firebase_admin import firestore
from datetime import datetime

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """
    Base repository implementing common CRUD operations.
    
    This class provides a template for database operations using Firebase Firestore.
    It implements the repository pattern to abstract data access logic.
    
    Attributes:
        collection_name: Name of the Firestore collection
        db: Firestore database instance
    
    Type Parameters:
        T: The model type this repository handles
    """
    
    def __init__(self, collection_name: str):
        """
        Initialize the repository.
        
        Args:
            collection_name: Name of the Firestore collection to use
        """
        self.collection_name = collection_name
        self.db = firestore.client()
        self.collection = self.db.collection(collection_name)

    async def create(self, data: Dict[str, Any]) -> T:
        """
        Create a new document in the collection.
        
        Args:
            data: Dictionary containing the document data
            
        Returns:
            T: Created document converted to model instance
            
        Raises:
            FirestoreError: If document creation fails
        """
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        
        doc_ref = self.collection.document()
        data['id'] = doc_ref.id
        doc_ref.set(data)
        
        return self._convert_to_model(data)

    async def get(self, id: str) -> Optional[T]:
        """
        Retrieve a document by ID.
        
        Args:
            id: Document ID
            
        Returns:
            Optional[T]: Document if found, None otherwise
            
        Raises:
            FirestoreError: If document retrieval fails
        """
        doc = self.collection.document(id).get()
        if doc.exists:
            return self._convert_to_model(doc.to_dict())
        return None

    async def get_all(self) -> List[T]:
        """
        Retrieve all documents in the collection.
        
        Returns:
            List[T]: List of all documents
            
        Raises:
            FirestoreError: If document retrieval fails
        """
        docs = self.collection.stream()
        return [self._convert_to_model(doc.to_dict()) for doc in docs]

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[T]:
        """
        Update a document by ID.
        
        Args:
            id: Document ID
            data: Dictionary containing the update data
            
        Returns:
            Optional[T]: Updated document if found, None otherwise
            
        Raises:
            FirestoreError: If document update fails
        """
        doc_ref = self.collection.document(id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return None
            
        data['updated_at'] = datetime.utcnow()
        doc_ref.update(data)
        
        updated_doc = doc_ref.get()
        return self._convert_to_model(updated_doc.to_dict())

    async def delete(self, id: str) -> bool:
        """
        Delete a document by ID.
        
        Args:
            id: Document ID
            
        Returns:
            bool: True if document was deleted, False if not found
            
        Raises:
            FirestoreError: If document deletion fails
        """
        doc_ref = self.collection.document(id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return False
            
        doc_ref.delete()
        return True

    async def find(self, filters: Dict[str, Any]) -> List[T]:
        """
        Find documents matching the specified filters.
        
        Args:
            filters: Dictionary of field-value pairs to filter by
            
        Returns:
            List[T]: List of matching documents
            
        Raises:
            FirestoreError: If query fails
        """
        query = self.collection
        
        for field, value in filters.items():
            query = query.where(field, '==', value)
            
        docs = query.stream()
        return [self._convert_to_model(doc.to_dict()) for doc in docs]

    def _convert_to_model(self, data: Dict[str, Any]) -> T:
        """
        Convert dictionary data to model instance.
        
        This method should be overridden by child classes to implement
        specific model conversion logic.
        
        Args:
            data: Dictionary containing document data
            
        Returns:
            T: Model instance
        """
        raise NotImplementedError("Subclasses must implement _convert_to_model")
