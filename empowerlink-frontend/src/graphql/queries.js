// src/graphql/queries.js
import { gql } from "@apollo/client";

// 1) Fetch current Inclusivity Index
export const GET_INCLUSIVITY_INDEX = gql`
  query computeInclusivityIndex($regionId: Int!) {
    computeInclusivityIndex(regionId: $regionId) {
      taskId
      status
    }
  }
`;

export const GET_TASK_STATUS = gql`
  query GetTaskStatus($taskId: String!) {
    getTaskStatus(taskId: $taskId) {
      value
      status
      error
    }
  }
`;

// 2) Fetch trend over time
export const GET_INCLUSIVITY_TREND = gql`
  query GetInclusivityTrend($regionId: Int!) {
    getInclusivityIndex(regionId: $regionId) {
      id
      value
      timestamp
    }
  }
`;

// // 2) Fetch trend over time
// export const GET_INCLUSIVITY_TREND = gql`
//   query GetInclusivityTrend($regionId: Int!) {
//     getInclusivityTrend(regionId: $regionId) {
//       id
//       value
//       timestamp
//     }
//   }
// `;

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

// 4) Get available resources (for list views)
export const GET_AVAILABLE_RESOURCES = gql`
  query GetAvailableResources($serviceType: String!, $location: GeoPointInput!) {
    getAvailableResources(serviceType: $serviceType, location: $location) {
      resourceId
      serviceType
      latitude
      longitude
      costLevel
    }
  }
`;

// 5) Request a resource match manually
export const REQUEST_RESOURCE_MATCH = gql`
  mutation RequestResourceMatching(
    $userId: ID!
    $serviceType: String!
    $location: GeoPointInput!
  ) {
    requestResourceMatching(
      userId: $userId
      serviceType: $serviceType
      location: $location
    ) {
      resource {
        resourceId
        serviceType
        latitude
        longitude
        costLevel
      }
      score
    }
  }
`;

// 6) Create a new resource (admin use)
export const CREATE_RESOURCE = gql`
  mutation CreateResource(
    $serviceType: String!
    $latitude: Float!
    $longitude: Float!
    $costLevel: Int!
  ) {
    createResource(
      serviceType: $serviceType
      latitude: $latitude
      longitude: $longitude
      costLevel: $costLevel
    ) {
      resourceId
      serviceType
      latitude
      longitude
      costLevel
    }
  }
`;

export const GET_RESOURCES_PER_CAPITA = gql`
  query GetResourcesPerCapita {
    resourcesPerCapita {
      regionId
      regionName
      category
      resourcesCount
      populationInNeed
      perThousandNeeded
    }
  }
`;

// 8) Get resource analytics: need gap
export const GET_RESOURCE_NEED_GAP = gql`
  query GetResourceNeedGap($regionId: Int!) {
    resourceNeedGap(regionId: $regionId) {
      serviceType
      gapValue
    }
  }
`;

// 9) Get resource analytics: match success rate
export const GET_MATCH_SUCCESS_RATE = gql`
  query GetMatchSuccessRate($regionId: Int!) {
    matchSuccessRate(regionId: $regionId) {
      serviceType
      successRate
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

// 5) Get USSD Menu
export const GET_USSD_MENU = gql`
  query GetUSSDMenu($phoneNumber: String!, $input: String!) {
    getUSSDMenu(phoneNumber: $phoneNumber, input: $input) {
      message
    }
  }
`;
