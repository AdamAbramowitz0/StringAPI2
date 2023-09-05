import stripe
import time
import uuid
import DBEdit
import schedule

def run():
        z = DBEdit.transactionPrep()
        for x in range(0,len(z)):
            keyNum = list(z.keys())[x]
            stripe.SubscriptionItem.create_usage_record(
                z[keyNum],
                quantity=int(keyNum/20),
                timestamp=int(time.time()),
                action='increment',
                idempotency_key = str(uuid.uuid4())
            )
        time.sleep(10)

schedule.every().day.at("20:49:59").do(run)

while True:
    schedule.run_pending()
    time.sleep(1)
