describe('Index', () => {
    it('display the page correctly if user is not logged in', () => {
        cy
          .visit('/')
          .get('h1').contains('All Users')
          .get('.navbar-burger').click()
          .get('a').contains('Signout').should('not.be.visible')
          .get('a').contains('Register')
          .get('a').contains('Login');
      });
});