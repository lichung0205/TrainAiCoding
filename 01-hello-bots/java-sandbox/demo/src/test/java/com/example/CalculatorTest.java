package com.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {

    private Calculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }

    @Test
    @DisplayName("測試加法 - 正數")
    void testAddPositiveNumbers() {
        // Arrange
        int a = 5;
        int b = 3;

        // Act
        int result = calculator.add(a, b);

        // Assert
        assertEquals(8, result, "5 + 3 應該等於 8");
    }

    @Test
    @DisplayName("測試加法 - 負數")
    void testAddNegativeNumbers() {
        assertEquals(-5, calculator.add(-2, -3));
    }

    @Test
    @DisplayName("測試加法 - 正數與負數")
    void testAddPositiveAndNegative() {
        assertEquals(2, calculator.add(5, -3));
    }

    @Test
    @DisplayName("測試加法 - 零")
    void testAddWithZero() {
        assertEquals(5, calculator.add(5, 0));
        assertEquals(0, calculator.add(0, 0));
    }

    @Test
    @DisplayName("測試減法 - 正數")
    void testSubPositiveNumbers() {
        assertEquals(2, calculator.sub(5, 3));
    }

    @Test
    @DisplayName("測試減法 - 負數")
    void testSubNegativeNumbers() {
        assertEquals(1, calculator.sub(-2, -3));
    }

    @Test
    @DisplayName("測試減法 - 正數與負數")
    void testSubPositiveAndNegative() {
        assertEquals(8, calculator.sub(5, -3));
    }

    @Test
    @DisplayName("測試減法 - 零")
    void testSubWithZero() {
        assertEquals(5, calculator.sub(5, 0));
        assertEquals(-5, calculator.sub(0, 5));
    }

    @ParameterizedTest
    @CsvSource({
            "1, 2, 3",
            "5, 10, 15",
            "-3, 7, 4",
            "0, 0, 0"
    })
    @DisplayName("參數化測試加法")
    void testAddParameterized(int a, int b, int expected) {
        assertEquals(expected, calculator.add(a, b));
    }

    @ParameterizedTest
    @CsvSource({
            "5, 2, 3",
            "10, 5, 5",
            "3, 7, -4",
            "0, 5, -5"
    })
    @DisplayName("參數化測試減法")
    void testSubParameterized(int a, int b, int expected) {
        assertEquals(expected, calculator.sub(a, b));
    }

    @Test
    @DisplayName("測試多個數字相加")
    void testAddMultipleNumbers() {
        assertEquals(15, calculator.addMultiple(1, 2, 3, 4, 5));
        assertEquals(0, calculator.addMultiple());
        assertEquals(10, calculator.addMultiple(10));
    }

    @ParameterizedTest
    @ValueSource(ints = { Integer.MAX_VALUE - 1, Integer.MIN_VALUE + 1 })
    @DisplayName("測試邊界值")
    void testBoundaryValues(int value) {
        // 測試加法邊界
        assertEquals(value + 1, calculator.add(value, 1));
        assertEquals(value - 1, calculator.sub(value, 1));
    }
}
