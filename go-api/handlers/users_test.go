package handlers

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestGetUser_ValidID(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/users/1", nil)
	req.SetPathValue("id", "1")
	w := httptest.NewRecorder()

	GetUser(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d", w.Code)
	}

	body := w.Body.String()
	if body == "" {
		t.Error("expected non-empty response body")
	}
}
