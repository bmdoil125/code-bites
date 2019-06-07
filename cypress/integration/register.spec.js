const randomstring = require('randomstring');

const username = randomstring.generate();
const email = `${username}@test.com`;

describe('Register', () => {
    it('display registration form', () => {
        cy
            .visit('/register')
            .get('h1').contains('Register')
            .get('form')
    });
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
});