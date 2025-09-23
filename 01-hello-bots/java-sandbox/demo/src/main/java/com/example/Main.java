package com.example;

// 產生一個可設定的簡單重試工具：重試次數、間隔、退避
public class Main {
    public static void main(String[] args) {
        RetryTool retryTool = new RetryTool(3, 1000, 2.0); // 最多重試3次，初始間隔1000ms，每次間隔*2
        try {
            String result = retryTool.execute(() -> {
                // 模擬可能失敗的操作
                if (Math.random() < 0.7) {
                    throw new RuntimeException("失敗");
                }
                return "成功";
            });
            System.out.println("結果：" + result);
        } catch (Exception e) {
            System.out.println("全部重試失敗：" + e.getMessage());
        }

        Calculator calobj = new Calculator();
        System.out.println("相加：" + calobj.add(2, 5));
        System.out.println("相減：" + calobj.sub(2, 5));
        System.out.println("多個相加：" + calobj.addMultiple(2, 5, 10));
    }
}
