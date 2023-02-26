import pika, json

from main import Recipe, db

params = pika.URLParameters('amqps://tyfodnmd:t0Ps2Jnw97Epl3YNe67zm2mjdDdir5Y8@rat.rmq2.cloudamqp.com/tyfodnmd')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='django') # this must match routing key of the Django microservice 


def callback(ch, method, properties, body):
    print('Received in Flask microservice')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'recipe_created':
        recipe = Recipe(id=data['id'], title=data['title'], time_minutes=data['time_minutes'], price=data['price'], description=data['description'], ingredients=data['ingredients'])
        db.session.add(recipe)
        db.session.commit()
        print('recipe Created')

    elif properties.content_type == 'recipe_updated':
        recipe = Recipe.query.get(data['id'])
        recipe.title = data['title']
        recipe.time_minutes = data['time_minutes']
        recipe.price = data['price']
        recipe.description = data['description']
        recipe.ingredients = data['ingredients']
        db.session.commit()
        print('recipe Updated')

    elif properties.content_type == 'recipe_deleted':
        recipe = Recipe.query.get(data)
        db.session.delete(recipe)
        db.session.commit()
        print('recipe Deleted')


channel.basic_consume(queue='django', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
