from fastapi import status


class Responses:
    class Errors:
        INVALID_OPERATION = {
            status.HTTP_400_BAD_REQUEST: {
                'description': 'Invalid operations',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'detail': {
                                    'type': 'string'
                                }
                            }
                        },
                        'examples': {
                            'fullAmountTooLow': {
                                'summary':
                                    'Full amount lower than invested amount',
                                'value': {
                                    'detail': (
                                        'Нельзя установить значение '
                                        'full_amount меньше уже'
                                        ' вложенной суммы.'
                                    )
                                }
                            },
                            'notUniqueName': {
                                'summary': 'Not unique name',
                                'value': {
                                    'detail': (
                                        'Проект с таким именем '
                                        'уже существует!'
                                    )
                                }
                            },
                            'projectClosed': {
                                'summary': 'Project closed',
                                'value': {
                                    'detail': (
                                        'Закрытый проект '
                                        'нельзя редактировать!'
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
        PROJECT_CLOSED_OR_WITH_DONATIONS = {
            status.HTTP_400_BAD_REQUEST: {
                'description': (
                    'Нельзя удалять закрытый проект или проект'
                    ', в который уже были инвестированы средства.'
                ),
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'detail': {
                                    'type': 'string'
                                }
                            }
                        },
                        'examples': {
                            'projectClosed': {
                                'summary': 'Project closed',
                                'value': {
                                    'detail': (
                                        'В проект были внесены средства'
                                        ', не подлежит удалению!'
                                    )
                                }
                            },
                            'projectWithDonations': {
                                'summary': 'Project with donations',
                                'value': {
                                    'detail': (
                                        'В проект были внесены средства'
                                        ', не подлежит удалению!'
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
        NOT_UNIQUE_NAME = {
            status.HTTP_400_BAD_REQUEST: {
                'description': 'Not unique name',
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'Проект с таким именем уже существует!'}
                    }
                }
            }
        }

        UNAUTHORIZED = {
            status.HTTP_401_UNAUTHORIZED: {
                'description': 'Missing token or inactive user',
                'content': {
                    'application/json': {
                        'example': {'detail': 'Unauthorized'}
                    }
                }
            }
        }

        FORBIDDEN = {
            status.HTTP_403_FORBIDDEN: {
                'description': 'Not a superuser',
                'content': {
                    'application/json': {
                        'example': {'detail': 'Forbidden'}
                    }
                }
            }
        }
