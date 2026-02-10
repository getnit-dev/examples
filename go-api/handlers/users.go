package handlers

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
	"strings"
)

type User struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

var users = map[int]User{
	1: {ID: 1, Name: "Alice", Email: "alice@example.com"},
	2: {ID: 2, Name: "Bob", Email: "bob@example.com"},
}

// GetUser retrieves a user by ID from the path parameter.
// Untested edge cases: non-numeric ID, negative ID, missing ID.
func GetUser(w http.ResponseWriter, r *http.Request) {
	idStr := r.PathValue("id")
	if idStr == "" {
		http.Error(w, "missing user id", http.StatusBadRequest)
		return
	}

	id, err := strconv.Atoi(idStr)
	if err != nil {
		http.Error(w, "invalid user id", http.StatusBadRequest)
		return
	}

	if id <= 0 {
		http.Error(w, "user id must be positive", http.StatusBadRequest)
		return
	}

	user, ok := users[id]
	if !ok {
		http.Error(w, "user not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(user)
}

// CreateUser adds a new user from the JSON request body.
// Untested edge cases: empty body, missing name, duplicate email, malformed JSON.
func CreateUser(w http.ResponseWriter, r *http.Request) {
	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
		http.Error(w, "invalid request body", http.StatusBadRequest)
		return
	}

	if strings.TrimSpace(user.Name) == "" {
		http.Error(w, "name is required", http.StatusBadRequest)
		return
	}

	if strings.TrimSpace(user.Email) == "" {
		http.Error(w, "email is required", http.StatusBadRequest)
		return
	}

	for _, existing := range users {
		if existing.Email == user.Email {
			http.Error(w, "email already exists", http.StatusConflict)
			return
		}
	}

	user.ID = len(users) + 1
	users[user.ID] = user

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(user)
}

// ValidateEmail checks whether a string looks like a valid email.
// Untested: no tests at all.
func ValidateEmail(email string) bool {
	if len(email) < 3 {
		return false
	}
	atIndex := strings.Index(email, "@")
	if atIndex < 1 {
		return false
	}
	dotIndex := strings.LastIndex(email, ".")
	if dotIndex < atIndex+2 {
		return false
	}
	if dotIndex >= len(email)-1 {
		return false
	}
	return true
}

// FormatUserDisplay returns a display-friendly string for a user.
// Untested: no tests at all.
func FormatUserDisplay(u User) string {
	if u.Name == "" {
		return fmt.Sprintf("User #%d (no name)", u.ID)
	}
	return fmt.Sprintf("%s <%s>", u.Name, u.Email)
}
