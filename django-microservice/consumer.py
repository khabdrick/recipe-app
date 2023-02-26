import pika, json, os, django
from django.http import JsonResponse
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipe.settings")
django.setup()

from app.models import Recipe, RecipeComment

params = pika.URLParameters('amqps://tyfodnmd:t0Ps2Jnw97Epl3YNe67zm2mjdDdir5Y8@rat.rmq2.cloudamqp.com/tyfodnmd')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='flask') # this will match the routing key in the producer of the flask app


def callback(ch, method, properties, body):
    print('Received in Django microservice')
    print(body)
    data = json.loads(body)
    # print(data)
    recipe_id = data[0]
    comment_text = data[1]
    recipe = Recipe.objects.get(pk=recipe_id)
    comment = RecipeComment(recipe=recipe, comment_text=comment_text)
    comment.save()
    print('Added a comment')


channel.basic_consume(queue='flask', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
