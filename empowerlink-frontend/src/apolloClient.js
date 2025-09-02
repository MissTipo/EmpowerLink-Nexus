import { ApolloClient, InMemoryCache, createHttpLink, ApolloLink } from '@apollo/client';

const loggingLink = new ApolloLink((operation, forward) => {
  console.log("🚀 GraphQL Request Body:", {
    operationName: operation.operationName,
    variables: operation.variables,
    context: operation.getContext(),
  });
  return forward(operation);
});

const httpLink = createHttpLink({
  uri: 'https://159.203.54.10.nip.io/graphql',
});

const client = new ApolloClient({
  link: ApolloLink.from([loggingLink,httpLink]),
  cache: new InMemoryCache(),
});

export default client;
