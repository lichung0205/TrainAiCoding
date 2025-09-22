package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MainTest {

    @Test
    void testSuccessOnFirstTry() throws Exception {
        RetryTool retryTool = new RetryTool(3, 10, 2.0);
        String result = retryTool.execute(() -> "OK");
        assertEquals("OK", result);
    }

    @Test
    void testSuccessAfterRetries() throws Exception {
        RetryTool retryTool = new RetryTool(3, 10, 2.0);
        final int[] count = { 0 };
        String result = retryTool.execute(() -> {
            if (count[0]++ < 2)
                throw new RuntimeException("fail");
            return "OK";
        });
        assertEquals("OK", result);
        assertEquals(3, count[0]);
    }

    @Test
    void testFailAfterMaxRetries() {
        RetryTool retryTool = new RetryTool(2, 10, 2.0);
        assertThrows(RuntimeException.class, () -> {
            retryTool.execute(() -> {
                throw new RuntimeException("always fail");
            });
        });
    }
}