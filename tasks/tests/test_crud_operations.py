# tasks/tests/test_crud_operations.py
"""
Simple unit tests for CRUD operations only.
Tests: Create, Read, Update, Delete
"""

import pytest
from django.urls import reverse
from tasks.models import Task
from datetime import date, timedelta


# =============================================================================
# CREATE OPERATION TESTS
# =============================================================================

@pytest.mark.django_db
class TestCreateOperation:
    """Tests for CREATE (adding new tasks)"""
    
    def test_create_task_via_view(self, authenticated_client, user):
        """Test creating a new task through the create view"""
        # Arrange - Prepare test data
        task_data = {
            'title': 'New Task',
            'description': 'Task Description',
            'status': 'pending',
            'priority': 'medium',
            'due_date': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')
        }
        
        # Act - Perform the create operation
        response = authenticated_client.post(reverse('task_create'), task_data)
        
        # Assert - Check results
        assert response.status_code == 302  # Redirects after success
        assert Task.objects.filter(user=user, title='New Task').exists()
        
        # Verify task was created with correct data
        task = Task.objects.get(user=user, title='New Task')
        assert task.description == 'Task Description'
        assert task.status == 'pending'
        assert task.priority == 'medium'
    
    def test_create_task_directly_in_model(self, user):
        """Test creating a task directly in the database"""
        # Act - Create task
        task = Task.objects.create(
            user=user,
            title='Direct Create Task',
            description='Created directly',
            status='pending',
            priority='high'
        )
        
        # Assert - Verify task exists
        assert task.pk is not None
        assert Task.objects.filter(pk=task.pk).exists()
    
    def test_create_task_count_increases(self, authenticated_client, user):
        """Test that creating a task increases the count"""
        # Arrange - Count existing tasks
        initial_count = Task.objects.filter(user=user).count()
        
        # Act - Create new task
        task_data = {
            'title': 'Count Test Task',
            'status': 'pending',
            'priority': 'low'
        }
        authenticated_client.post(reverse('task_create'), task_data)
        
        # Assert - Count increased by 1
        final_count = Task.objects.filter(user=user).count()
        assert final_count == initial_count + 1


# =============================================================================
# READ OPERATION TESTS
# =============================================================================

@pytest.mark.django_db
class TestReadOperation:
    """Tests for READ (viewing/listing tasks)"""
    
    def test_read_task_list(self, authenticated_client, user):
        """Test reading list of all tasks"""
        # Arrange - Create test tasks
        Task.objects.create(user=user, title='Task 1')
        Task.objects.create(user=user, title='Task 2')
        Task.objects.create(user=user, title='Task 3')
        
        # Act - Get task list
        response = authenticated_client.get(reverse('task_list'))
        
        # Assert - Check response
        assert response.status_code == 200
        content = str(response.content)
        assert 'Task 1' in content
        assert 'Task 2' in content
        assert 'Task 3' in content
    
    def test_read_single_task_detail(self, authenticated_client, user):
        """Test reading a single task's details"""
        # Arrange - Create a task
        task = Task.objects.create(
            user=user,
            title='Detail Test Task',
            description='Detailed description',
            status='in_progress',
            priority='high'
        )
        
        # Act - Get task detail
        response = authenticated_client.get(reverse('task_detail', args=[task.pk]))
        
        # Assert - Check task details are displayed
        assert response.status_code == 200
        content = str(response.content)
        assert 'Detail Test Task' in content
        assert 'Detailed description' in content
    
    def test_read_task_from_database(self, user):
        """Test reading a task directly from database"""
        # Arrange - Create task
        created_task = Task.objects.create(
            user=user,
            title='DB Read Test'
        )
        
        # Act - Read task from database
        retrieved_task = Task.objects.get(pk=created_task.pk)
        
        # Assert - Verify data matches
        assert retrieved_task.title == 'DB Read Test'
        assert retrieved_task.user == user
    
    def test_read_empty_task_list(self, authenticated_client):
        """Test reading task list when no tasks exist"""
        # Act - Get empty task list
        response = authenticated_client.get(reverse('task_list'))
        
        # Assert - Page loads successfully
        assert response.status_code == 200


# =============================================================================
# UPDATE OPERATION TESTS
# =============================================================================

@pytest.mark.django_db
class TestUpdateOperation:
    """Tests for UPDATE (editing existing tasks)"""
    
    def test_update_task_via_view(self, authenticated_client, user):
        """Test updating a task through the update view"""
        # Arrange - Create original task
        task = Task.objects.create(
            user=user,
            title='Original Title',
            description='Original Description',
            status='pending',
            priority='low'
        )
        
        # Act - Update the task
        update_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'status': 'completed',
            'priority': 'high',
            'due_date': (date.today() + timedelta(days=14)).strftime('%Y-%m-%d')
        }
        response = authenticated_client.post(
            reverse('task_update', args=[task.pk]),
            update_data
        )
        
        # Assert - Check update was successful
        assert response.status_code == 302  # Redirects after success
        
        # Verify task was updated
        task.refresh_from_db()
        assert task.title == 'Updated Title'
        assert task.description == 'Updated Description'
        assert task.status == 'completed'
        assert task.priority == 'high'
    
    def test_update_task_directly_in_model(self, user):
        """Test updating a task directly in the database"""
        # Arrange - Create task
        task = Task.objects.create(
            user=user,
            title='Before Update',
            status='pending'
        )
        
        # Act - Update task
        task.title = 'After Update'
        task.status = 'completed'
        task.save()
        
        # Assert - Verify update
        updated_task = Task.objects.get(pk=task.pk)
        assert updated_task.title == 'After Update'
        assert updated_task.status == 'completed'
    
    def test_update_only_one_field(self, authenticated_client, user):
        """Test updating only one field of a task"""
        # Arrange - Create task
        task = Task.objects.create(
            user=user,
            title='Partial Update Test',
            description='Original Description',
            status='pending',
            priority='medium'
        )
        
        # Act - Update only status
        update_data = {
            'title': 'Partial Update Test',
            'description': 'Original Description',
            'status': 'completed',  # Only this changed
            'priority': 'medium'
        }
        authenticated_client.post(
            reverse('task_update', args=[task.pk]),
            update_data
        )
        
        # Assert - Verify only status changed
        task.refresh_from_db()
        assert task.status == 'completed'
        assert task.description == 'Original Description'  # Unchanged


# =============================================================================
# DELETE OPERATION TESTS
# =============================================================================

@pytest.mark.django_db
class TestDeleteOperation:
    """Tests for DELETE (removing tasks)"""
    
    def test_delete_task_via_view(self, authenticated_client, user):
        """Test deleting a task through the delete view"""
        # Arrange - Create task to delete
        task = Task.objects.create(
            user=user,
            title='Task to Delete'
        )
        task_pk = task.pk
        
        # Act - Delete the task
        response = authenticated_client.post(reverse('task_delete', args=[task_pk]))
        
        # Assert - Check deletion was successful
        assert response.status_code == 302  # Redirects after success
        assert not Task.objects.filter(pk=task_pk).exists()
    
    def test_delete_task_directly_from_model(self, user):
        """Test deleting a task directly from database"""
        # Arrange - Create task
        task = Task.objects.create(
            user=user,
            title='Direct Delete Test'
        )
        task_pk = task.pk
        
        # Act - Delete task
        task.delete()
        
        # Assert - Verify task is gone
        assert not Task.objects.filter(pk=task_pk).exists()
    
    def test_delete_task_count_decreases(self, authenticated_client, user):
        """Test that deleting a task decreases the count"""
        # Arrange - Create tasks and count them
        task1 = Task.objects.create(user=user, title='Task 1')
        task2 = Task.objects.create(user=user, title='Task 2')
        initial_count = Task.objects.filter(user=user).count()
        
        # Act - Delete one task
        authenticated_client.post(reverse('task_delete', args=[task1.pk]))
        
        # Assert - Count decreased by 1
        final_count = Task.objects.filter(user=user).count()
        assert final_count == initial_count - 1
        assert Task.objects.filter(pk=task2.pk).exists()  # Other task still exists
    
    def test_delete_nonexistent_task(self, authenticated_client):
        """Test deleting a task that doesn't exist"""
        # Act - Try to delete non-existent task
        response = authenticated_client.post(reverse('task_delete', args=[99999]))
        
        # Assert - Should return 404
        assert response.status_code == 404


# =============================================================================
# COMPLETE CRUD WORKFLOW TEST
# =============================================================================

@pytest.mark.django_db
class TestCompleteCRUDWorkflow:
    """Test complete CRUD workflow: Create → Read → Update → Delete"""
    
    def test_full_crud_lifecycle(self, authenticated_client, user):
        """Test complete CRUD lifecycle of a task"""
        
        # 1. CREATE - Create a new task
        create_data = {
            'title': 'CRUD Workflow Task',
            'description': 'Testing full lifecycle',
            'status': 'pending',
            'priority': 'medium'
        }
        response = authenticated_client.post(reverse('task_create'), create_data)
        assert response.status_code == 302
        
        task = Task.objects.get(user=user, title='CRUD Workflow Task')
        assert task is not None
        
        # 2. READ - Read the created task
        response = authenticated_client.get(reverse('task_detail', args=[task.pk]))
        assert response.status_code == 200
        assert 'CRUD Workflow Task' in str(response.content)
        
        # 3. UPDATE - Update the task
        update_data = {
            'title': 'CRUD Workflow Task (Updated)',
            'description': 'Updated description',
            'status': 'completed',
            'priority': 'high'
        }
        response = authenticated_client.post(
            reverse('task_update', args=[task.pk]),
            update_data
        )
        assert response.status_code == 302
        
        task.refresh_from_db()
        assert task.title == 'CRUD Workflow Task (Updated)'
        assert task.status == 'completed'
        
        # 4. DELETE - Delete the task
        task_pk = task.pk
        response = authenticated_client.post(reverse('task_delete', args=[task_pk]))
        assert response.status_code == 302
        assert not Task.objects.filter(pk=task_pk).exists()


# =============================================================================
# SUMMARY OF CRUD TESTS
# =============================================================================
"""
Total CRUD Tests: 16 tests

CREATE Tests (3):
- test_create_task_via_view
- test_create_task_directly_in_model
- test_create_task_count_increases

READ Tests (4):
- test_read_task_list
- test_read_single_task_detail
- test_read_task_from_database
- test_read_empty_task_list

UPDATE Tests (3):
- test_update_task_via_view
- test_update_task_directly_in_model
- test_update_only_one_field

DELETE Tests (4):
- test_delete_task_via_view
- test_delete_task_directly_from_model
- test_delete_task_count_decreases
- test_delete_nonexistent_task

COMPLETE WORKFLOW Test (1):
- test_full_crud_lifecycle

Run these tests:
pytest tasks/tests/test_crud_operations.py -v
"""
