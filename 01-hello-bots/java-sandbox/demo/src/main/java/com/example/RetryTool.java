package com.example;

import java.util.function.Supplier;

public class RetryTool {
    private final int maxRetries;
    private final long initialDelayMillis;
    private final double backoffFactor;

    public RetryTool(int maxRetries, long initialDelayMillis, double backoffFactor) {
        this.maxRetries = maxRetries;
        this.initialDelayMillis = initialDelayMillis;
        this.backoffFactor = backoffFactor;
    }

    public <T> T execute(Supplier<T> action) throws Exception {
        long delay = initialDelayMillis;
        for (int attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                return action.get();
            } catch (Exception e) {
                if (attempt == maxRetries) {
                    throw e;
                }
                Thread.sleep(delay);
                delay = (long) (delay * backoffFactor);
            }
        }
        throw new Exception("重試失敗");
    }
}
