import pytest
import sys
import os
from unittest.mock import MagicMock

# Mock pygame before importing snake
sys.modules['pygame'] = MagicMock()

# Add the parent directory to the path so we can import snake
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from snake import move_snake, check_collision, check_eating, WIDTH, HEIGHT, CELL

def test_move_snake():
    head = (100, 100)
    # Test moving right
    assert move_snake(head, CELL, 0) == (120, 100)
    # Test moving down
    assert move_snake(head, 0, CELL) == (100, 120)
    # Test moving left
    assert move_snake(head, -CELL, 0) == (80, 100)
    # Test moving up
    assert move_snake(head, 0, -CELL) == (100, 80)

def test_check_collision_walls():
    # Test left wall
    assert check_collision((-CELL, 100), []) == True
    # Test right wall
    assert check_collision((WIDTH, 100), []) == True
    # Test top wall
    assert check_collision((100, -CELL), []) == True
    # Test bottom wall
    assert check_collision((100, HEIGHT), []) == True
    # Test inside bounds
    assert check_collision((100, 100), []) == False

def test_check_collision_self():
    head = (100, 100)
    body = [(100, 100), (80, 100)]
    assert check_collision(head, body) == True
    
    body_safe = [(80, 100), (60, 100)]
    assert check_collision(head, body_safe) == False

def test_check_eating():
    head = (100, 100)
    food = (100, 100)
    assert check_eating(head, food) == True
    
    food_far = (200, 200)
    assert check_eating(head, food_far) == False
