from tickets.utils import ChoiceEnum


class Urgency(ChoiceEnum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
