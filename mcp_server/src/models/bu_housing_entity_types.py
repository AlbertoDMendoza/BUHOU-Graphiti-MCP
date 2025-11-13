"""Custom entity type definitions for Boston University Housing Knowledge Graph.

This module defines entity types aligned with Common Core Ontology (CCO) terminology
for better interoperability and semantic consistency.

CCO Alignment:
- Role (BU Affiliation) → cco:Role (derived from BDO:Role or similar)
- LocationArea → cco:Site (top-level geographic/campus area)
- Facility (Building) → cco:Facility (individual buildings)
- FloorOrSuite → cco:Facility (floor or suite subdivision)
- Room → cco:Facility (individual room within floor/suite)
- RoomSpace → cco:Facility (bed space within room)
- AmenityFacility → cco:Facility (shared amenities)
- Agreement → cco:Agreement
- ServiceRequest → cco:ServiceRequest (Information Content Entity)
- Assignment → cco:Directive (Information Content Entity)
- Policy → cco:Policy (Directive Information Content Entity)
- Application → cco:Application (Information Content Entity)
- Event → cco:Act
- FinancialTransaction → cco:Act

BU Housing Spatial Hierarchy:
Location Area → Building → Floor/Suite → Room → Room Space

Privacy Note:
This ontology is designed to be PII-free. No personal names, IDs, or contact information
are stored. Instead, we capture organizational roles and responsibilities.
"""

from pydantic import BaseModel, Field


class Role(BaseModel):
    """A Role represents a functional position or responsibility in the BU Housing context.

    CCO Alignment: cco:Role - A realizable entity realized by a person in virtue of some process
    BU Context: Aligned with BU's "Affiliation" concept (student, employee, faculty, affiliate, alumni)
    Domain Context: Housing-related roles without storing PII

    Privacy Design: This entity type stores NO PII (no names, IDs, contact info).
    Instead, it captures the role, responsibilities, and organizational context.

    Instructions for identifying and extracting roles:
    1. Identify the affiliation type (employee, student, faculty, affiliate, alumni)
    2. For employees: Extract job title (RA, RD, Maintenance Staff, Coordinator, etc.)
    3. For employees: Note department/unit (Residential Life, Facilities, Housing Admin, etc.)
    4. For students: Capture role in housing (resident, peer advisor, student worker)
    5. Track responsibilities or scope of role
    6. Note building or area of responsibility when applicable
    7. Avoid capturing any personal identifiers - focus on the role itself
    8. Capture role status (active, inactive, temporary, permanent)
    9. Include any special designations (lead RA, senior staff, etc.)
    """

    affiliation_type: str = Field(
        ...,
        description='BU affiliation type (employee, student, faculty, affiliate, alumni)',
    )
    job_title: str | None = Field(
        None,
        description='Job title or position (RA, RD, Maintenance Technician, Housing Coordinator, etc.)',
    )
    department: str | None = Field(
        None,
        description='Department or organizational unit (Residential Life, Facilities, Housing Admin, etc.)',
    )
    responsibilities: str | None = Field(
        None,
        description='Key responsibilities or scope of the role',
    )
    assigned_location: str | None = Field(
        None,
        description='Building, floor, or area where role is performed (if applicable)',
    )
    role_status: str | None = Field(
        None,
        description='Status of the role (active, inactive, temporary, permanent)',
    )


class LocationArea(BaseModel):
    """A LocationArea represents a top-level geographic or campus housing area.

    CCO Alignment: cco:Site - A geographic region designated for a particular purpose
    Domain Context: High-level housing area grouping (Student Village, Bay State Road Apartments, West Campus, etc.)

    Hierarchy Level: 1 of 5 (LocationArea → Building → Floor/Suite → Room → Room Space)

    Instructions for identifying and extracting location areas:
    1. Identify named campus housing areas or neighborhoods
    2. Examples: "Student Village", "Bay State Road Apartments", "West Campus", "South Campus"
    3. Note geographic boundaries or campus location
    4. Capture distinguishing characteristics of the area
    5. Track area-wide amenities or features
    6. Include proximity to academic buildings or transit
    7. Note overall capacity or number of buildings in area
    8. Identify special designations (undergraduate-only, graduate housing, etc.)
    """

    name: str = Field(
        ...,
        description='Name of the location area (e.g., "Student Village", "Bay State Road Apartments")',
    )
    campus_location: str | None = Field(
        None,
        description='Geographic location on campus (East Campus, West Campus, Central, etc.)',
    )
    description: str | None = Field(
        None,
        description='Description of the area and its characteristics',
    )
    area_amenities: str | None = Field(
        None,
        description='Shared amenities available across the location area',
    )
    special_designation: str | None = Field(
        None,
        description='Special area designation (undergraduate, graduate, family housing, etc.)',
    )


class Facility(BaseModel):
    """A Facility (Building) represents an individual residence hall or housing building.

    CCO Alignment: cco:Facility - A Site that has been designed to support some particular Processual Entity
    Domain Context: Individual building within a location area (e.g., "10 Buick Street", "Kilachand Hall", "Warren Towers")

    Hierarchy Level: 2 of 5 (LocationArea → Building → Floor/Suite → Room → Room Space)

    Instructions for identifying and extracting buildings:
    1. Identify specific building names or addresses (e.g., "10 Buick Street", "Kilachand Hall")
    2. Extract building street address when available
    3. Note building type (traditional dorm, apartment-style, brownstone, tower)
    4. Capture total capacity or number of floors
    5. Identify building-specific amenities (lobby, elevators, dining hall, laundry)
    6. Track accessibility features (ADA accessible, elevator access)
    7. Note parent location area (which campus area it belongs to)
    8. Include year built or major renovation dates if mentioned
    9. Capture special building characteristics (honors housing, LLC, themed communities)
    """

    name: str = Field(
        ...,
        description='Building name or identifier (e.g., "10 Buick Street", "Kilachand Hall")',
    )
    street_address: str | None = Field(
        None,
        description='Street address of the building',
    )
    location_area: str | None = Field(
        None,
        description='Parent location area (e.g., "Student Village", "Bay State Road Apartments")',
    )
    building_type: str | None = Field(
        None,
        description='Type of building (traditional dorm, apartment-style, brownstone, tower, etc.)',
    )
    total_capacity: int | None = Field(
        None,
        description='Total number of residents the building can house',
    )
    number_of_floors: int | None = Field(
        None,
        description='Number of floors in the building',
    )
    building_amenities: str | None = Field(
        None,
        description='Building-specific amenities (lobby, elevators, dining hall, laundry, etc.)',
    )
    accessibility_features: str | None = Field(
        None,
        description='Accessibility features (ADA accessible, elevator access, ramps, etc.)',
    )
    special_designation: str | None = Field(
        None,
        description='Special building designation (honors housing, LLC, themed community, etc.)',
    )
    year_built: str | None = Field(
        None,
        description='Year the building was constructed or last renovated',
    )


class FloorOrSuite(BaseModel):
    """A FloorOrSuite represents a floor level or suite subdivision within a building.

    CCO Alignment: cco:Facility - A subdivision of a building designed to organize living spaces
    Domain Context: Floor or suite within a building (e.g., "10 Buick-0101", "Floor 3", "Suite A")

    Hierarchy Level: 3 of 5 (LocationArea → Building → Floor/Suite → Room → Room Space)

    Instructions for identifying and extracting floors or suites:
    1. Identify floor numbers or suite identifiers (e.g., "10 Buick-0101", "Floor 3", "Suite A")
    2. Note parent building
    3. Capture floor/suite type (standard floor, suite, apartment cluster)
    4. Track number of rooms on floor/in suite
    5. Identify shared spaces (bathrooms, kitchens, common areas)
    6. Note floor-specific features (study lounge, quiet floor designation)
    7. Include accessibility information for the floor/suite
    8. Track capacity at floor/suite level
    9. Capture any special designations (honors floor, themed floor, substance-free)
    """

    identifier: str = Field(
        ...,
        description='Floor or suite identifier (e.g., "10 Buick-0101", "Floor 3", "Suite A")',
    )
    building_name: str = Field(
        ...,
        description='Parent building name',
    )
    floor_number: int | None = Field(
        None,
        description='Floor number within building',
    )
    subdivision_type: str | None = Field(
        None,
        description='Type of subdivision (floor, suite, apartment cluster, etc.)',
    )
    number_of_rooms: int | None = Field(
        None,
        description='Number of rooms on this floor/in this suite',
    )
    shared_spaces: str | None = Field(
        None,
        description='Shared spaces available (bathrooms, kitchen, common room, etc.)',
    )
    floor_amenities: str | None = Field(
        None,
        description='Floor/suite-specific amenities (study lounge, laundry, etc.)',
    )
    special_designation: str | None = Field(
        None,
        description='Special floor/suite designation (quiet floor, honors, themed, substance-free, etc.)',
    )


class Room(BaseModel):
    """A Room represents an individual room within a floor or suite.

    CCO Alignment: cco:Facility - An individual living space within a building
    Domain Context: Individual room (e.g., "Room 101", "10 Buick-0101-A")

    Hierarchy Level: 4 of 5 (LocationArea → Building → Floor/Suite → Room → Room Space)

    Instructions for identifying and extracting rooms:
    1. Identify room numbers (e.g., "Room 101", "10 Buick-0101-A")
    2. Note parent floor/suite and building
    3. Capture room type (single, double, triple, quad, studio)
    4. Track total capacity (number of bed spaces)
    5. Identify room features (private bathroom, kitchenette, balcony)
    6. Note square footage or room size if available
    7. Track furniture provided (beds, desks, chairs, closets)
    8. Include accessibility features (ADA compliant, grab bars, etc.)
    9. Capture view or window information if relevant
    """

    room_number: str = Field(
        ...,
        description='Room number or identifier (e.g., "Room 101", "10 Buick-0101-A")',
    )
    floor_or_suite: str = Field(
        ...,
        description='Parent floor or suite identifier',
    )
    building_name: str = Field(
        ...,
        description='Parent building name',
    )
    room_type: str | None = Field(
        None,
        description='Type of room (single, double, triple, quad, studio, etc.)',
    )
    capacity: int | None = Field(
        None,
        description='Total capacity (number of bed spaces in room)',
    )
    square_footage: int | None = Field(
        None,
        description='Room size in square feet',
    )
    room_features: str | None = Field(
        None,
        description='Room features (private bathroom, kitchenette, balcony, etc.)',
    )
    furniture_provided: str | None = Field(
        None,
        description='Furniture included (beds, desks, chairs, closets, etc.)',
    )
    accessibility_features: str | None = Field(
        None,
        description='Accessibility features (ADA compliant, grab bars, lowered fixtures, etc.)',
    )


class RoomSpace(BaseModel):
    """A RoomSpace represents an individual bed space within a room.

    CCO Alignment: cco:Facility - An individual occupancy space within a room
    Domain Context: Bed space or occupancy position (e.g., "101A", "101B", "Bed 1")

    Hierarchy Level: 5 of 5 (LocationArea → Building → Floor/Suite → Room → Room Space)

    Instructions for identifying and extracting room spaces:
    1. Identify bed space designators (e.g., "101A", "101B", "Bed 1", "Space A")
    2. Note parent room, floor/suite, and building
    3. Track space type (lofted bed, standard bed, accessible space)
    4. Capture space-specific features (window access, desk location, closet access)
    5. Note furniture configuration for this space
    6. Include any accessibility accommodations for this specific space
    7. Track space status (occupied, vacant, reserved)
    8. Identify special accommodations (medical, accessibility, ESA approved)
    """

    space_identifier: str = Field(
        ...,
        description='Space identifier within room (e.g., "101A", "101B", "Bed 1", "Space A")',
    )
    room_number: str = Field(
        ...,
        description='Parent room number',
    )
    floor_or_suite: str = Field(
        ...,
        description='Parent floor or suite identifier',
    )
    building_name: str = Field(
        ...,
        description='Parent building name',
    )
    space_type: str | None = Field(
        None,
        description='Type of space (lofted bed, standard bed, accessible space, etc.)',
    )
    space_features: str | None = Field(
        None,
        description='Space-specific features (window access, desk location, closet access, etc.)',
    )
    furniture_items: str | None = Field(
        None,
        description='Furniture items for this specific space (bed, desk, chair, dresser, etc.)',
    )
    accessibility_accommodations: str | None = Field(
        None,
        description='Accessibility or special accommodations for this space',
    )
    space_status: str | None = Field(
        None,
        description='Status of the space (occupied, vacant, reserved, maintenance, etc.)',
    )


class Agreement(BaseModel):
    """An Agreement represents a housing contract or lease between BU Housing and a student.

    CCO Alignment: cco:Agreement - A Directive Information Content Entity that prescribes mutual commitments
    Domain Context: Housing lease, contract, or housing agreement

    Instructions for identifying and extracting agreements:
    1. Look for contract terms, housing agreements, or lease mentions
    2. Extract start and end dates (academic year, semester, summer)
    3. Identify payment terms and amounts
    4. Note contract type (academic year, semester, summer, year-round)
    5. Capture any special terms or conditions
    6. Track contract status (active, pending, cancelled, completed)
    7. Include cancellation policy details if mentioned
    8. Note any deposits or fees required
    9. Identify housing assignment tied to the lease
    """

    contract_id: str | None = Field(
        None,
        description='Unique identifier for the lease/contract',
    )
    contract_type: str = Field(
        ...,
        description='Type of lease (academic year, semester, summer, year-round)',
    )
    start_date: str | None = Field(
        None,
        description='Lease start date',
    )
    end_date: str | None = Field(
        None,
        description='Lease end date',
    )
    payment_amount: str | None = Field(
        None,
        description='Total payment amount or rent',
    )
    terms: str | None = Field(
        None,
        description='Special terms, conditions, or policies of the lease',
    )
    status: str | None = Field(
        None,
        description='Contract status (active, pending, cancelled, completed)',
    )


class ServiceRequest(BaseModel):
    """A ServiceRequest represents a work order, repair request, or service ticket for housing facilities.

    CCO Alignment: cco:Information Content Entity - An entity that encodes information about a requested service
    Domain Context: Maintenance request, repair ticket, work order, or service request

    Instructions for identifying and extracting service requests:
    1. Look for mentions of repairs, fixes, work orders, or maintenance needs
    2. Extract request ID or ticket number if provided
    3. Identify the issue type (plumbing, electrical, HVAC, appliance, etc.)
    4. Capture priority level (emergency, urgent, routine)
    5. Note location (building, unit number) where work is needed
    6. Track status (submitted, in progress, completed, cancelled)
    7. Include submitter information if mentioned
    8. Note any deadline or completion date
    9. Capture resolution details when work is completed
    """

    request_id: str | None = Field(
        None,
        description='Unique identifier for the maintenance request',
    )
    issue_type: str = Field(
        ...,
        description='Type of maintenance issue (plumbing, electrical, HVAC, etc.)',
    )
    description: str = Field(
        ...,
        description='Detailed description of the maintenance issue',
    )
    priority: str | None = Field(
        None,
        description='Priority level (emergency, urgent, routine)',
    )
    location: str = Field(
        ...,
        description='Building and unit where maintenance is needed',
    )
    status: str | None = Field(
        None,
        description='Current status (submitted, in progress, completed, cancelled)',
    )
    submitted_date: str | None = Field(
        None,
        description='Date the request was submitted',
    )


class AmenityFacility(BaseModel):
    """An AmenityFacility represents a facility, service location, or shared resource available to BU Housing residents.

    CCO Alignment: cco:Facility - A Site designed to provide amenities or services
    Domain Context: Gym, laundry room, study lounge, mail room, or other shared facilities

    Instructions for identifying and extracting amenity facilities:
    1. Look for mentions of facilities (gym, laundry, study rooms, lounges)
    2. Identify services (mail room, package pickup, bike storage)
    3. Extract location (building-specific or shared across campus)
    4. Note access requirements or restrictions
    5. Capture hours of operation if mentioned
    6. Track capacity or availability
    7. Include any fees or costs associated with use
    8. Note amenity condition or recent updates
    9. Identify popular or highly-used amenities
    """

    name: str = Field(
        ...,
        description='Name of the amenity or facility',
    )
    amenity_type: str = Field(
        ...,
        description='Type of amenity (gym, laundry, study room, lounge, parking, etc.)',
    )
    location: str = Field(
        ...,
        description='Building or location where amenity is available',
    )
    access_details: str | None = Field(
        None,
        description='Access requirements, hours, or restrictions',
    )
    features: str | None = Field(
        None,
        description='Specific features or equipment available',
    )


class Assignment(BaseModel):
    """An Assignment represents the allocation of a role to a specific housing unit.

    CCO Alignment: cco:Directive Information Content Entity - An ICE prescribing an allocation or assignment
    Domain Context: Room assignment, housing placement, or unit allocation

    Privacy Design: References roles, not individuals. No PII stored.

    Instructions for identifying and extracting assignments:
    1. Identify the role type being assigned (resident, RA, student worker, etc.)
    2. Extract assignment dates (move-in, move-out dates)
    3. Identify bed space or specific location within unit
    4. Note assignment status (confirmed, pending, waitlisted)
    5. Capture any special requirements or accommodations needed for the role
    6. Include lottery numbers or priority rankings (if applicable)
    7. Note assignment method (lottery, selection, appointment)
    8. Track changes or reassignments with reasons
    9. Avoid capturing any personal identifiers
    """

    role_type: str = Field(
        ...,
        description='Type of role being assigned (resident, RA, RD, student worker, etc.)',
    )
    unit_number: str = Field(
        ...,
        description='Room/unit number being assigned',
    )
    building_name: str = Field(
        ...,
        description='Building where the assignment is located',
    )
    assignment_period: str = Field(
        ...,
        description='Time period for the assignment (Fall 2024, Spring 2025, etc.)',
    )
    move_in_date: str | None = Field(
        None,
        description='Scheduled move-in date',
    )
    move_out_date: str | None = Field(
        None,
        description='Scheduled move-out date',
    )
    status: str | None = Field(
        None,
        description='Assignment status (confirmed, pending, waitlisted, cancelled)',
    )


class Policy(BaseModel):
    """A Policy represents rules, regulations, or guidelines for BU Housing residents.

    CCO Alignment: cco:Policy - A Directive Information Content Entity that prescribes actions or behaviors
    Domain Context: Housing rules, regulations, conduct codes, or guidelines

    Instructions for identifying and extracting policies:
    1. Look for mentions of rules, regulations, or guidelines
    2. Identify policy categories (guests, quiet hours, pets, smoking, etc.)
    3. Extract specific requirements or restrictions
    4. Note consequences or penalties for violations
    5. Capture effective dates or policy changes
    6. Include any exceptions or special circumstances
    7. Track policy enforcement methods
    8. Note which buildings or residents are affected
    9. Identify safety policies and emergency procedures
    """

    policy_name: str = Field(
        ...,
        description='Name or title of the policy',
    )
    category: str = Field(
        ...,
        description='Policy category (guests, quiet hours, pets, alcohol, safety, etc.)',
    )
    description: str = Field(
        ...,
        description='Detailed description of the policy rules and requirements',
    )
    applies_to: str | None = Field(
        None,
        description='Who or what the policy applies to (all residents, specific buildings, etc.)',
    )
    consequences: str | None = Field(
        None,
        description='Consequences or penalties for policy violations',
    )


class Application(BaseModel):
    """An Application represents a housing application or request for BU Housing.

    CCO Alignment: cco:Information Content Entity - An ICE that encodes an application or request
    Domain Context: Housing application, lottery submission, or housing request

    Privacy Design: Application details without applicant PII. Links to roles, not individuals.

    Instructions for identifying and extracting applications:
    1. Identify application type (new student, returning student, transfer, staff housing)
    2. Capture housing preferences ranked in order
    3. Note accommodation requirements (accessibility, special needs)
    4. Track application status and timeline
    5. Include lottery number or priority ranking (without linking to specific person)
    6. Note roommate matching preferences (by criteria, not names)
    7. Identify any deposits or fees associated
    8. Track application method (online portal, paper, special process)
    9. Avoid capturing personal identifiers - focus on application characteristics
    """

    application_type: str = Field(
        ...,
        description='Type of application (new student, returning, transfer, staff housing, etc.)',
    )
    applicant_role: str | None = Field(
        None,
        description='Role type of applicant (student, employee, faculty, etc.)',
    )
    preferences: str | None = Field(
        None,
        description='Housing preferences in ranked order (building types, locations, room types)',
    )
    accommodation_needs: str | None = Field(
        None,
        description='Special accommodation or accessibility requirements',
    )
    roommate_criteria: str | None = Field(
        None,
        description='Roommate matching preferences (study habits, schedule, interests - no names)',
    )
    status: str | None = Field(
        None,
        description='Application status (submitted, under review, approved, denied, waitlisted)',
    )
    submission_date: str | None = Field(
        None,
        description='Date the application was submitted',
    )
    lottery_number: str | None = Field(
        None,
        description='Lottery or priority number (anonymized)',
    )


class Event(BaseModel):
    """An Event represents activities, inspections, or occurrences in BU Housing.

    CCO Alignment: cco:Act - A Processual Entity performed by an Agent
    Domain Context: Housing events, inspections, incidents, or scheduled activities

    Instructions for identifying and extracting events:
    1. Look for scheduled events (move-in day, orientation, community events)
    2. Identify inspections (room checks, fire safety, move-out inspections)
    3. Extract incident reports or violations
    4. Note building closures or maintenance windows
    5. Capture event date, time, and location
    6. Track attendance or participation requirements
    7. Include event purpose and expected outcomes
    8. Note any follow-up actions required
    9. Identify mandatory vs. optional events
    """

    event_name: str = Field(
        ...,
        description='Name or title of the event',
    )
    event_type: str = Field(
        ...,
        description='Type of event (move-in, inspection, community event, incident, etc.)',
    )
    date: str | None = Field(
        None,
        description='Date and time of the event',
    )
    location: str = Field(
        ...,
        description='Building or specific location of the event',
    )
    description: str = Field(
        ...,
        description='Detailed description of the event',
    )
    mandatory: bool | None = Field(
        None,
        description='Whether attendance is mandatory',
    )


class FinancialTransaction(BaseModel):
    """A FinancialTransaction represents financial transactions and payments related to BU Housing.

    CCO Alignment: cco:Act - A Processual Entity involving exchange of money
    Domain Context: Rent payments, deposits, fees, refunds, or housing-related charges

    Privacy Design: Transaction details without payer identity. References roles or facilities, not individuals.

    Instructions for identifying and extracting financial transactions:
    1. Identify transaction type (rent, deposit, damage fee, late fee, refund, etc.)
    2. Extract transaction amounts (avoid linking to specific individuals)
    3. Capture transaction date and due date
    4. Note payment method category (bursar account, online payment, etc.)
    5. Track transaction status (pending, completed, overdue, refunded)
    6. Include transaction reference numbers (anonymized)
    7. Note associated facility or unit (not individual resident)
    8. Track payment plans or installment arrangements at aggregate level
    9. Avoid capturing payer names or personal identifiers
    """

    transaction_id: str | None = Field(
        None,
        description='Unique transaction identifier (anonymized)',
    )
    amount: str = Field(
        ...,
        description='Transaction amount',
    )
    transaction_type: str = Field(
        ...,
        description='Type of transaction (rent, deposit, damage fee, late fee, refund, etc.)',
    )
    associated_unit: str | None = Field(
        None,
        description='Associated housing unit or facility (not individual)',
    )
    due_date: str | None = Field(
        None,
        description='Payment due date',
    )
    transaction_date: str | None = Field(
        None,
        description='Date transaction was processed',
    )
    payment_method_type: str | None = Field(
        None,
        description='Type of payment method (bursar account, online, etc.)',
    )
    status: str | None = Field(
        None,
        description='Transaction status (pending, completed, overdue, refunded)',
    )


# Registry of all BU Housing entity types (CCO-aligned, PII-free)
# Organized by hierarchy level and function
BU_HOUSING_ENTITY_TYPES: dict[str, type[BaseModel]] = {
    # Roles and People (PII-free)
    'Role': Role,  # BU Affiliations and functional roles

    # Spatial Hierarchy (5 levels)
    'LocationArea': LocationArea,  # Level 1: Campus housing areas (Student Village, Bay State Road)
    'Facility': Facility,  # Level 2: Buildings (10 Buick Street, Kilachand Hall)
    'FloorOrSuite': FloorOrSuite,  # Level 3: Floors or suites (10 Buick-0101, Floor 3)
    'Room': Room,  # Level 4: Individual rooms (Room 101, 10 Buick-0101-A)
    'RoomSpace': RoomSpace,  # Level 5: Bed spaces (101A, 101B, Bed 1)

    # Amenities
    'AmenityFacility': AmenityFacility,  # Shared facilities and amenities

    # Operational Entities
    'Agreement': Agreement,  # Leases and housing contracts
    'ServiceRequest': ServiceRequest,  # Maintenance and service requests
    'Assignment': Assignment,  # Role-to-space assignments (PII-free)
    'Policy': Policy,  # Housing policies and regulations
    'Application': Application,  # Housing applications (PII-free)
    'Event': Event,  # Housing events and occurrences
    'FinancialTransaction': FinancialTransaction,  # Financial transactions (PII-free)
}
