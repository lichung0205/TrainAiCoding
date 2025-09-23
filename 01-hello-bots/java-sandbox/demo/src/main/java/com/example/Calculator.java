package com.example;

public class Calculator {

    /**
     * 加法運算
     * 
     * @param a 第一個運算元
     * @param b 第二個運算元
     * @return 兩數之和
     */
    public int add(int a, int b) {
        return a + b;
    }

    /**
     * 減法運算
     * 
     * @param a 被減數
     * @param b 減數
     * @return 兩數之差
     */
    public int sub(int a, int b) {
        return a - b;
    }

    /**
     * 加法運算（支援多個參數）
     * 
     * @param numbers 要相加的數字
     * @return 所有數字之和
     */
    public int addMultiple(int... numbers) {
        int sum = 0;
        for (int num : numbers) {
            sum += num;
        }
        return sum;
    }
}
