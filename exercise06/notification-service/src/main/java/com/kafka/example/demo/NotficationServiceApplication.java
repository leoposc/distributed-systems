package com.kafka.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class NotficationServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(NotficationServiceApplication.class, args);
	}

	@KafkaListener(id = "myGroup", topics = "order-topic")
	public void listen(String in) {
	//Logic to consume/process message goes here
	System.out.println(in);
	}
}
