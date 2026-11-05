import pytest
from django.db.migrations.state import ProjectState

from django_test_migrations.migrator import Migrator


@pytest.mark.django_db
def test_migrator(transactional_db):
    """We only need this test for coverage."""
    migrator = Migrator()
    old_state = migrator.apply_initial_migration(('main_app', None))
    new_state = migrator.apply_tested_migration(('main_app', '0001_initial'))

    assert isinstance(old_state, ProjectState)
    assert isinstance(new_state, ProjectState)
    assert migrator.reset() is None


@pytest.mark.django_db
def test_migrator_list(transactional_db):
    """We only need this test for coverage."""
    migrator = Migrator()
    old_state = migrator.apply_initial_migration([('main_app', None)])
    new_state = migrator.apply_tested_migration([('main_app', '0001_initial')])

    assert isinstance(old_state, ProjectState)
    assert isinstance(new_state, ProjectState)
    assert migrator.reset() is None


@pytest.mark.django_db
def test_collect_leaf_nodes_no_conflict(transactional_db):
    """Check to see if, with one migration per app, it collects that migration"""
    migrator = Migrator()
    target = ('main_app', '0001_initial')
    collected = migrator.collect_leaf_nodes(target)

    assert target in collected


@pytest.mark.django_db
def test_collect_leaf_nodes_with_conflict(transactional_db):
    """Check to see if, with multiple migrations per app, it collects the last"""
    migrator = Migrator()
    target_1 = ('main_app', '0001_initial')
    target_2 = ('main_app', '0002_someitem_is_clean')
    collected = migrator.collect_leaf_nodes([target_1, target_2])

    assert target_1 not in collected
    assert target_2 in collected
