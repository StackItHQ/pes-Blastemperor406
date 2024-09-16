use superjoin;
show tables;
CREATE TABLE cars (
    id INT PRIMARY KEY,
    Name VARCHAR(50),
    Color VARCHAR(50),
    Model VARCHAR(50),
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

select * from cars;