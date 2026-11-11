#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from dataclasses import FrozenInstanceError

import pytest

from domain.exceptions import ValidationError
from domain.value_objects import (
    Login,
    Password,
    RoleName,
    Search,
    PageLimit,
    Batch
)


class TestLogin:
    @pytest.mark.parametrize("value", ["a", "john_doe", "Іван-Петренко", "o'neil", "x" * 32])
    def test_accepts_valid(self, value):
        assert Login(value).value == value

    @pytest.mark.parametrize("value", ["", "x" * 33, "john@doe", "<script>", "tab\tname"])
    def test_rejects_invalid(self, value):
        with pytest.raises(ValidationError):
            Login(value)

    def test_is_immutable(self):
        login = Login("john")

        with pytest.raises(FrozenInstanceError):
            login.value = "other"


class TestPassword:
    @pytest.mark.parametrize("value", ["abc", "Secret 123!", "пароль123", "x" * 64])
    def test_accepts_valid(self, value):
        assert Password(value).value == value

    @pytest.mark.parametrize("value", ["", "ab", " abc", "abc ", "x" * 65, "abc\x00def"])
    def test_rejects_invalid(self, value):
        with pytest.raises(ValidationError):
            Password(value)


class TestRoleName:
    def test_equality_by_value(self):
        assert RoleName("admin") == RoleName("admin")
        assert RoleName("admin") != RoleName("user")

    @pytest.mark.parametrize("value", ["", "x" * 33, "admin!"])
    def test_rejects_invalid(self, value):
        with pytest.raises(ValidationError):
            RoleName(value)


class TestPagination:
    @pytest.mark.parametrize("value", [1, 50, 100])
    def test_page_limit_accepts_range(self, value):
        assert PageLimit(value).value == value

    @pytest.mark.parametrize("value", [0, -1, 101])
    def test_page_limit_rejects_out_of_range(self, value):
        with pytest.raises(ValidationError):
            PageLimit(value)

    @pytest.mark.parametrize("value", ["", "x" * 129])
    def test_search_rejects_invalid_length(self, value):
        with pytest.raises(ValidationError):
            Search(value)

    def test_batch_accepts_up_to_100_items(self):
        assert len(Batch(list(range(100))).value) == 100

    @pytest.mark.parametrize("value", [[], list(range(101))])
    def test_batch_rejects_invalid_size(self, value):
        with pytest.raises(ValidationError):
            Batch(value)
