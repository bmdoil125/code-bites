const randomstring = require('randomstring');

const username = randomstring.generate();
const email = `${username}@test.com`;


describe('Profile', () => {
    it('should not display user info if a user is not logged in', () => {
        cy
          .visit('/me')
          .get('p').contains('You must be logged in to view this page.')
          .get('a').contains('Signout').should('not.be.visible')
          .get('a').contains('Register')
          .get('a').contains('Log In');
      });
      it('display user info if a user is logged in', () => {
        // register user
        cy
          .visit('/register')
          .get('input[name="username"]').type(username)
          .get('input[name="email"]').type(email)
          .get('input[name="password"]').type('test')
          .get('input[type="submit"]').click()
          .get('.navbar-burger').click();
      
        cy.wait(500);
      
        // assert '/me' is displayed properly
        cy.visit('/me');
        cy.get('.navbar-burger').click();
        cy.contains('Profile').click();
        cy.get('li > strong').contains('User ID:')
          .get('li > strong').contains('Email:')
          .get('li').contains(email)
          .get('li > strong').contains('Username:')
          .get('li').contains(username)
          .get('a').contains('Profile')
          .get('a').contains('Signout')
          .get('a').contains('Register').should('not.be.visible')
          .get('a').contains('Login').should('not.be.visible');
    });

});