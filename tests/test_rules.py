from league_table.rules import FIRST_DIVISION_1974_75, MODERN_ENGLISH_LEAGUE


def test_1974_75_points_are_two_for_a_win():
    assert FIRST_DIVISION_1974_75.points_win == 2
    assert FIRST_DIVISION_1974_75.points_draw == 1
    assert FIRST_DIVISION_1974_75.points_loss == 0


def test_modern_rules_are_three_for_a_win():
    assert MODERN_ENGLISH_LEAGUE.points_win == 3


def test_points_for_mixed_record():
    # 3 wins, 2 draws, 1 loss under 1974/75 rules: 3*2 + 2*1 + 1*0 = 8
    assert FIRST_DIVISION_1974_75.points_for(won=3, drawn=2, lost=1) == 8


def test_points_for_mixed_record_modern():
    # 3 wins, 2 draws, 1 loss under modern rules: 3*3 + 2*1 + 1*0 = 11
    assert MODERN_ENGLISH_LEAGUE.points_for(won=3, drawn=2, lost=1) == 11
