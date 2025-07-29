import os

import bjoern

from {{ project_name }}.wsgi import application

bjoern.listen(
    application,
    '0.0.0.0',
    int(os.environ.get('PORT', 8080)),
)
bjoern.run()

