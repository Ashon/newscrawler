from core.app import initialize_applictaion

import settings


app = initialize_applictaion(settings)

from core.tasks import DistributeChain
from tasks.harvest import Harvest
from tasks.extract import Extract
from tasks.aggregate import Aggregate

app.register_task(DistributeChain())
app.register_task(Harvest())
app.register_task(Extract())
app.register_task(Aggregate())
