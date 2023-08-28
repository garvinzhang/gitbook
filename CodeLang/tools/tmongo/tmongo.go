package tmongo

import (
	"context"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func InitMongo(uri string) (client *mongo.Client, err error) {
	clientOptions := options.Client().ApplyURI(uri) //"mongodb://localhost:27017"
	client, err = mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		return
	}
	err = client.Ping(context.TODO(), nil)
	if err != nil {
		return
	}
	return
}
