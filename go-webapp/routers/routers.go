package routers

import (
	"Covid-19-Report/handlers"

	"github.com/gorilla/mux"
)

func SetRouter() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/", handlers.RootHandler)
	r.HandleFunc("/generate-report", handlers.GenerateReport)
	return r
}
