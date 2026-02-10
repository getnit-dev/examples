package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {

    private final Calculator calc = new Calculator();

    @Test
    void testAddPositiveNumbers() {
        assertEquals(5, calc.add(2, 3));
        assertEquals(0, calc.add(0, 0));
    }

    @Test
    void testSubtractBasic() {
        assertEquals(1, calc.subtract(3, 2));
    }
}
