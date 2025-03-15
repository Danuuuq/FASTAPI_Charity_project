class Responses:
    class Errors:
        INVALID_OPERATION = {
            400: {
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
            400: {
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
            400: {
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
            401: {
                'description': 'Missing token or inactive user',
                'content': {
                    'application/json': {
                        'example': {'detail': 'Unauthorized'}
                    }
                }
            }
        }

        FORBIDDEN = {
            403: {
                'description': 'Not a superuser',
                'content': {
                    'application/json': {
                        'example': {'detail': 'Forbidden'}
                    }
                }
            }
        }
