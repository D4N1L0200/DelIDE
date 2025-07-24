import math
import geometry as geo

if __name__ == "__main__":
    assert geo.area(5) == math.pi * 5**2
    assert geo.circumference(5) == 2 * math.pi * 5
    assert geo.PI == math.pi
    print("All tests passed!")
