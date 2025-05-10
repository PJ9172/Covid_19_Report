package main

import (
	"Covid-19-Report/routers"
	"log"
	"net/http"
)

func main() {

	r := routers.SetRouter()

	log.Println("Server Starts on Port 3000!!!")
	log.Println(http.ListenAndServe(":3000", r))
}
