package main

import (
  "fmt"
  "strings"
  "net/http"
  "io/ioutil"
)

func main() {

  url := "https://api.venafi.cloud/outagedetection/v1/certificates"
  method := "GET"

  payload := strings.NewReader(`{
    "expression": {
        "operator": "AND",
        "operands": [
            {
                "operator": "AND",
                "operands": [
                    {
                        "operator": "OR",
                        "operands": [
                            {
                                "field": "certificateStatus",
                                "operator": "EQ",
                                "value": "ACTIVE"
                            }
                        ]
                    }
                ]
            },
            {
                "operator": "OR",
                "operands": [
                    {
                        "field": "certificateStatus",
                        "operator": "EQ",
                        "value": "ACTIVE"
                    }
                ]
            },
            {
                "operator": "OR",
                "operands": [
                    {
                        "field": "extendedKeyUsage",
                        "values": [
                            "1.3.6.1.5.5.7.3.1"
                        ],
                        "operator": "MATCH"
                    }
                ]
            },
            {
                "operator": "OR",
                "operands": [
                    {
                        "field": "issuerCN",
                        "values": [
                            "Amazon"
                        ],
                        "operator": "MATCH"
                    }
                ]
            }
        ]
    },
    "ordering": {
        "orders": [
            {
                "direction": "DESC",
                "field": "certificatInstanceModificationDate"
            }
        ]
    },
    "paging": {
        "pageNumber": 0,
        "pageSize": 50
    }
}`)

  client := &http.Client {
  }
  req, err := http.NewRequest(method, url, payload)

  if err != nil {
    fmt.Println(err)
    return
  }
  req.Header.Add("tppl-api-key", "27b20743-2ddc-418d-8c84-0b3fb2ff066a")
  req.Header.Add("accept", "application/json")
  req.Header.Add("Content-Type", "application/json")

  res, err := client.Do(req)
  if err != nil {
    fmt.Println(err)
    return
  }
  defer res.Body.Close()

  body, err := ioutil.ReadAll(res.Body)
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println(string(body))
}