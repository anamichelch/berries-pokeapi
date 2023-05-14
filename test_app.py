from app import get_berries_names, get_growth_time, get_all_growth_times, get_frequency_growth_time


def test_get_berries_names():
    assert len(get_berries_names()) == 64

def test_get_growth_time():
    time = get_growth_time("cheri")
    assert time == 3


def test_get_all_growth_times():
    berries = ["cheri", "chesto","pecha","rawst","aspear"]
    times = get_all_growth_times(berries)
    assert times == [3,3,3,3,3]

def test_get_frequency_growth_time():
    # Test with sample growth time data
    growth_times = [3, 3, 6, 6, 10]
    freq = get_frequency_growth_time(growth_times)
    assert freq == {3: 2, 6: 2, 10: 1}