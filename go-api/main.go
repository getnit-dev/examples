package main

import (
	"fmt"
	"net/http"

	"example.com/go-api/handlers"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /users/{id}", handlers.GetUser)
	mux.HandleFunc("POST /users", handlers.CreateUser)

	fmt.Println("Server starting on :8080")
	if err := http.ListenAndServe(":8080", mux); err != nil {
		fmt.Printf("Failed to start server: %v\n", err)
	}
}
