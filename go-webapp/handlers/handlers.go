package handlers

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"net/http"
	"text/template"
)
type RequestBody struct{
	Country string `json:"country"`
}

func RootHandler(w http.ResponseWriter, r *http.Request) {
	temp, _ := template.ParseFiles("templates/index.html")
	temp.Execute(w, nil)
}

func GenerateReport(w http.ResponseWriter, r *http.Request) {
	country := r.FormValue("country")
	reqBody := RequestBody{
		Country : country,
	}
	reqjson, _ := json.Marshal(reqBody)

	res, err := http.Post("http://localhost:5000/generate-report", "application/json", bytes.NewBuffer(reqjson))
	if err != nil{
		http.Error(w,"Error to post request!!!", http.StatusInternalServerError)
		return
	}
	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)
	w.Write(body)
	
}
