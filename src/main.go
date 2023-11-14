package main

import (
	"github.com/gin-gonic/gin"
)

func main() {
	// create gin-router
	router := gin.Default()

	// define endpoint
	router.GET("/api/v2/assets/status", func(c *gin.Context) {
		c.JSON(
			200,
			gin.H{
				"authors": []string{
					"Nico Merkel",
					"Leon Richter",
				},
				"supported apis": []string{},
			},
		)
	})

	// start server
	err := router.Run(":8081")
	if err != nil {
		return
	}
}
