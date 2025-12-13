class DB:
    data = {}

    async def cast_text_to_vector(self, text) -> 'Vector':
        return ''

    async def search_by_vector(self, vector) -> dict:
        return {'count': 1, 'response': ''}

    async def search(self, text) -> dict:
        """
        {
        'text',
        'request_count',
        'last_requested'
        }
        """
        vector = self.cast_text_to_vector(text)
        search_res = self.search_by_vector(vector)


