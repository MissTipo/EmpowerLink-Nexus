// src/components/UserProfile.js
import React from 'react';
import { useQuery, gql } from '@apollo/client';

const GET_USER_PROFILE = gql`
  query GetUserProfile($id: ID!) {
    getUserProfile(id: $id) {
      id
      name
      gender
      age
      location
    }
  }
`;

const UserProfile = () => {
  const { loading, error, data } = useQuery(GET_USER_PROFILE, {
    variables: { id: "1" }, // Test with a sample user ID
  });

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error fetching user profile</p>;

  // Log the data to the console
  console.log(data);

  // const { id, name, gender, age, location } = data.getUserProfile;

  // return (
  //   <div>
  //     <h2>User Profile</h2>
  //     <p>ID: {id}</p>
  //     <p>Name: {name}</p>
  //     <p>Gender: {gender}</p>
  //     <p>Age: {age}</p>
  //     <p>Location: {location}</p>
  //   </div>
  // );
  // If data exists, render it
  if (data && data.getUserProfile) {
    const { id, name, gender, age, location } = data.getUserProfile;
    return (
      <div>
        <h2>User Profile</h2>
        <p>ID: {id}</p>
        <p>Name: {name}</p>
        <p>Gender: {gender}</p>
        <p>Age: {age}</p>
        <p>Location: {location}</p>
      </div>
    );
  }

  return <p>No user profile data available</p>;
};

export default UserProfile;

