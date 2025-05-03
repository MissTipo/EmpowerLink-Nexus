// src/apolloClient.js
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';

const httpLink = createHttpLink({
  // uri: 'http://127.0.0.1:8000/graphql/', // Adjust the URL as needed
  uri: 'http://35.238.68.232.nip.io/graphql/', // Adjust the URL as needed
});

const client = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
});

export default client;

