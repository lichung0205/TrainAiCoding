## 建立一個 demo 的 maven 專案
該專案會自動生成 main & test

當中的 pom 要做以下設定

<properties>
    <maven.compiler.release>17</maven.compiler.release>
    <junit.jupiter.version>5.10.2</junit.jupiter.version>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
</properties>

<dependencies>
    <!-- JUnit 5：測試用 -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>${junit.jupiter.version}</version>
        <scope>test</scope>
    </dependency>
</dependencies>

<build>
    <plugins>
        <!-- Surefire 3.x 會自動啟用 JUnit Platform -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.2.5</version>
            <configuration>
                <useModulePath>false</useModulePath>
            </configuration>
        </plugin>
    </plugins>
</build>


# MainTest 要移到 test\java\com\example 才符合測試檔案

## 最後操作指令 
mvn test

## 執行範例
mvn compile exec:java -Dexec.mainClass="com.example.Main"
