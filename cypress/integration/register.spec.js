const randomstring = require('randomstring');

const username = randomstring.generate();
const email = `${username}@test.com`;

describe('Register', () => {
    it('display registration form', () => {
        cy
            .visit('/register')
            .get('h1').contains('Register')
            .get('form')
            .get('input[disabled')
            .get('.validation-list')
            .get('.validation-list > error').first().contains(
                'Username must be greater than 5 characters.');
    });
    it('allow a user to register', () => {
        cy
            .visit('/register')
            .get('input[name="username"]').type(username)
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type('test')
            .get('input[type="submit"]').click()
            
    // Expect redirect to "/"
        cy.contains('All Users')
        cy.contains(username)
        cy.get('.navbar-burger').click()
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('Profile')
                .get('.navbar-item').contains('Signout')
                .get('.navbar-item').contains('Login').should('not.be.visible')
                .get('.navbar-item').contains('Register').should('not.be.visible');
        })
    })
    it('validate the password field', () => {
        cy
          .visit('/register')
          .get('h1').contains('Register')
          .get('form')
          .get('input[disabled]')
          .get('.validation-list > .error').contains(
            'Password must be greater than 10 characters.')
          .get('input[name="password"]').type('greaterthanten')
          .get('.validation-list')
          .get('.validation-list > .error').contains(
            'Password must be greater than 10 characters.').should('not.be.visible')
          .get('.validation-list > .success').contains(
            'Password must be greater than 10 characters.');
        cy.get('.navbar-burger').click();
        cy.get('.navbar-item').contains('Log In').click();
        cy.get('.navbar-item').contains('Register').click();
        cy.get('.validation-list > .error').contains(
            'Password must be greater than 10 characters.');
      });
});