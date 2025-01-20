package com.kafka.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;



@Component
public class MessageProducer {
	private final KafkaTemplate<String, String> kafkaTemplate;

	public MessageProducer(KafkaTemplate<String, String> kafkaTemplate) {
		this.kafkaTemplate = kafkaTemplate;
	}

	public void send(String message) {
		this.kafkaTemplate.send("order-topic", message);
	}
}

@SpringBootApplication
@RestController
public class OrderServiceApplication {
	
	@Autowired
	Environment env;
	
	@Autowired
	MessageProducer messageProducer;
	
	public static void main(String[] args) {
		SpringApplication.run(OrderServiceApplication.class, args);
	}

	@PostMapping("/notify")
	public String sendNotifation(@RequestBody String message){
		System.out.println("sending message : " + message);
		messageProducer.send(message);
		System.out.println("Sent message : " + message);
		return message;
	}
}
