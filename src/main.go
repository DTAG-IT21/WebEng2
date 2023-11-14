package main

import (
	"github.com/gin-gonic/gin"
)

func main() {
	// create gin-router
	router := gin.Default()

	// define endpoints
	router.GET("/api/v2/assets/status", authors)

	// start server
	err := router.Run(":8081")
	if err != nil {
		return
	}
}

func authors(c *gin.Context) {
	c.JSON(200, map[string][]string{
		"authors":       {"Nico Merkel", "Leon Richter"},
		"supportedApis": {"jwt-v2", "assets-v2", "reservations-v2"},
	})
}
