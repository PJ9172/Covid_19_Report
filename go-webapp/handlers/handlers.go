package handlers

import (
	"bytes"
	"encoding/json"
	"html/template"
	"io/ioutil"
	"net/http"
)

type RequestBody struct {
	Country string `json:"country"`
}
type ResponseBody struct {
	Country           string `json:"country"`
	Confirmed         string `json:"confirmed"`
	Deaths            string `json:"deaths"`
	Recovered         string `json:"recovered"`
}

func RootHandler(w http.ResponseWriter, r *http.Request) {
	temp, _ := template.ParseFiles("templates/index.html")
	temp.Execute(w, nil)
}

func GenerateReport(w http.ResponseWriter, r *http.Request) {
	country := r.FormValue("country")
	reqBody := RequestBody{Country: country}
	reqjson, _ := json.Marshal(reqBody)

	res, err := http.Post("http://127.0.0.1:5000/report", "application/json", bytes.NewBuffer(reqjson))
	if err != nil {
		http.Error(w, "Error to post request!!!", http.StatusInternalServerError)
		return
	}
	defer res.Body.Close()

	var data ResponseBody
	body, _ := ioutil.ReadAll(res.Body)
	json.Unmarshal(body, &data)

	// Convert to JSON string for JS
	jsonData, _ := json.Marshal(data)
	// fmt.Println(string(jsonData))

	// Pass both raw struct and JSON string
	tmplData := struct {
		RawData       ResponseBody
		CovidDataJSON template.JS
	}{
		RawData:       data,
		CovidDataJSON: template.JS(jsonData),
	}

	temp, _ := template.ParseFiles("templates/result.html")
	temp.Execute(w, tmplData)
}
