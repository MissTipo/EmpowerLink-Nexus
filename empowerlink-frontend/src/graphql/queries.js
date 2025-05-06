// src/graphql/queries.js
import { gql } from "@apollo/client";

// 1) Fetch current Inclusivity Index
export const GET_INCLUSIVITY_INDEX = gql`
  query computeInclusivityIndex($regionId: Int!) {
    computeInclusivityIndex(regionId: $regionId) {
      value
    }
  }
`;

// 2) Fetch trend over time
export const GET_INCLUSIVITY_TREND = gql`
  query GetInclusivityTrend($regionId: Int!) {
    getInclusivityTrend(regionId: $regionId) {
      value
    }
  }
`;

// 3) Fetch resource matches
export const GET_RESOURCE_MATCHES = gql`
  query GetResourceMatches(
    $userId: ID!
    $serviceType: ServiceType!
    $location: GeoPointInput!
    $limit: Int
  ) {
    getMatchingResources(
      userId: $userId
      serviceType: $serviceType
      location: $location
      limit: $limit
    ) {
      resource {
        resource_id
        service_type
        latitude
        longitude
        cost_level
      }
      score
    }
  }
`;

// 4) Subscribe to index updates via WebSocket (if your gateway exposes a subscription)
export const SUBSCRIBE_TO_INDEX = gql`
  subscription OnIndexUpdate($regionId: Int!) {
    indexUpdated(regionId: $regionId) {
      current
      trend { month value }
    }
  }
`;

