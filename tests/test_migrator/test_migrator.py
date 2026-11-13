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
def test_migrator_target_name_exact(transactional_db):
    """Ensures we get the same migration specified."""
    migrator = Migrator()
    target = ('main_app', '0001_initial')

    assert migrator._identify_target_migrations([target]) == [target]


@pytest.mark.django_db
def test_migrator_target_name_none(transactional_db):
    """Ensures None targes are returned."""
    migrator = Migrator()
    target = ('main_app', None)

    assert migrator._identify_target_migrations([target]) == [target]


@pytest.mark.django_db
def test_migrator_target_name_prefix(transactional_db):
    """Ensures prefixes are translated."""
    migrator = Migrator()
    target = ('main_app', '0001_initial')

    assert migrator._identify_target_migrations([('main_app', '0001')]) == [target]


@pytest.mark.django_db
def test_migrator_target_name_first(transactional_db):
    """Ensures __first__ is translated."""
    migrator = Migrator()
    target = ('main_app', '0001_initial')

    assert migrator._identify_target_migrations([('main_app', '__first__')]) == [target]


@pytest.mark.django_db
def test_migrator_target_name_latest(transactional_db):
    """Ensures __latest__ is translated."""
    migrator = Migrator()
    target = ('main_app', '0006_fix_through_fields')

    assert migrator._identify_target_migrations([('main_app', '__latest__')]) == [target]
