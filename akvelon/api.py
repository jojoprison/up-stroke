class CustomErr(Exception):
    pass

class API:

    async def give_response(
            self, request, db
    ) -> dict:

        text = request.json()

        try:
            task_id = await db.search(text)
        except CustomErr:
            return {
                'message': 'Продолжаем поиск',
                'is_init_state': True
            }
        except Exception:
            return {'message': 'Что-то упало, попытка еще раз'}

        return {
            'message': 'started',
            'task_id': task_id
        }

    def search_status(self, task_id) -> dict:
        pass

    def get_response(
            self, task_id
    ) -> bytearray:
        pass

