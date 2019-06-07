describe('Index', () => {
    it('users can view the index "/"', () => {
        cy
            .visit('/')
            .get('h1').contains('All Users')
    });
});