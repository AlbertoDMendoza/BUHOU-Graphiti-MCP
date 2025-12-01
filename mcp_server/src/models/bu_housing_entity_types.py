"""Custom entity type definitions for Boston University Housing Knowledge Graph.

This module defines entity types aligned with Common Core Ontology (CCO) terminology
for better interoperability and semantic consistency.

KNOWLEDGE GRAPH DESIGN PRINCIPLES:
====================================
1. FLEXIBILITY OVER RIGIDITY: Entity types should be flexible enough to represent both 
   abstract types and concrete instances. Let relationships capture specificity.
   
2. RELATIONSHIPS > FIELDS: When information varies or has multiple values, use graph 
   relationships instead of entity fields. Examples:
   - Event locations → (:Event)-[:LOCATED_AT]->(:Facility)
   - Term containment → (:Term {name: "Fall 2025"})-[:PART_OF]->(:Term {name: "AY 2024-25"})
   - Role assignments → (:Role)-[:ASSIGNED_TO]->(:Facility)
   
3. TYPE VS. INSTANCE: Many entities can represent both types and instances:
   - Type: (Event {name: "Graduation"}) - the general concept
   - Instance: (Event {name: "Spring 2025 Graduation"})-[:INSTANCE_OF]->(Event {name: "Graduation"})
   Use the same entity type for both; relationships clarify the distinction.
   
4. GRADUAL SPECIFICITY: Start minimal, add detail through edges as needed. Don't force 
   completeness upfront with required fields.
   
5. PRIVACY NOTE: This ontology is designed to be PII-free. No personal names, IDs, or contact information
   are stored. Instead, we capture organizational roles and responsibilities.

CCO ALIGNMENT:
==============
- Term → cco:TemporalRegion (time intervals with cultural/administrative significance)
- Role (BU Affiliation) → cco:Role (derived from BDO:Role or similar)
- LocationArea → cco:Site (top-level geographic/campus area)
- Building → cco:Facility (individual buildings)
- FloorOrSuite → cco:Facility (floor or suite subdivision)
- Room/RoomBase → cco:Facility (individual room within floor/suite)
- RoomSpace → cco:Facility (bed space within room)


BU HOUSING SPATIAL HIERARCHY:
=============================
Location Area → Building → Floor/Suite → Room/RoomBase → Room Space

"""

from pydantic import BaseModel, Field


# ============================================================================
# TEMPORAL ENTITIES
# ============================================================================
# NOTE ON EVENT:
# ==============
# Use the generic Event from original Graphiti (name, description only) which is flexible 
# enough for knowledge graph representation.
# Graphiti captures event specifics through relationships rather than rigid schema fields.
# Example Event Patterns in KG:
# - (:Event {name: "Graduation"})-[:OCCURS_IN]->(:Term {name: "Spring"})
# - (:Event {name: "Fall 2025 Move-In"})-[:INSTANCE_OF]->(:Event {name: "Move-In Day"})
# - (:Event)-[:LOCATED_AT]->(:Facility)
# - (:Event)-[:MANAGED_BY]->(:Role)


class Term(BaseModel):
    """A Term represents a temporal period or academic/administrative time interval.
    
    CCO Alignment: cco:TemporalRegion - A portion of time with defined boundaries
    Domain Context: Academic terms, fiscal periods, and administrative time periods.
    
    TYPE VS. INSTANCE FLEXIBILITY:
    This entity can represent both term types and specific term instances:
    - Type: (Term {name: "Fall Semester", term_type: "semester"})
    - Instance: (Term {name: "Fall 2025", term_type: "semester", start_date: "2025-09-01"})
    
    RELATIONSHIP PATTERNS FOR TERMS:
    1. Hierarchical containment:
       (:Term {name: "Fall 2025"})-[:PART_OF]->(:Term {name: "AY 2024-25"})
       
    2. Sequential ordering:
       (:Term {name: "Fall 2025"})-[:PRECEDES]->(:Term {name: "Spring 2025"})
       
    3. Event timing:
       (:Event {name: "Move-In Day"})-[:OCCURS_DURING]->(:Term {name: "Fall 2025"})
       
    4. Agreement periods:
       (:Agreement)-[:VALID_DURING]->(:Term {name: "AY 2024-25"})
       
    5. Assignment periods:
       (:Assignment)-[:FOR_TERM]->(:Term {name: "Spring 2025"})
    
    Common BU Housing Terminology:
    - Calendar Types: "Academic Calendar", "Fiscal Calendar", "Administrative Calendar"
    - Academic Calendar: "Fall Semester", "Spring Semester", "Summer Session I", "Summer Session II"
    - Academic Years: "AY 2024-25", "AY 2025-26"
        * Academic Year starts in Summer, then Fall, then Spring.
        * Academic Calendar is defined here: https://www.bu.edu/reg/calendars/
    - Fiscal Year: "FY2025", "Q1 FY2025"
        * Fiscal Year starts 1st of June goes until end of May. 
    - Administrative Calendar:
        * University Holidays and Intersession are listed here: https://www.bu.edu/calendar/holidays.html
    - Generic terms: "Fall Term", "Spring Term", "Summer Term"
    - Term Session: "Fall 2025", "Spring 2026"

    
    Instructions for identifying and extracting terms:
    1. Look for named time periods (Fall 2025, Spring 2025, AY 2024-25)
    2. Identify generic term types (Fall Semester, Summer Session)
    3. Extract start/end dates when mentioned (optional for generic types)
    4. Note term type (semester, academic_year, summer_session, fiscal_year, quarter)
    5. Capture any special characteristics (intersession, extended term)
    6. For specific instances, include the year
    7. For generic types, omit dates to allow reuse across years
    8. Use relationships to express containment (Fall 2025 is part of AY 2025-26)
    """
    
    name: str = Field(
        ...,
        description='Name of the term (e.g., "Fall 2025", "AY 2024-25", "Summer Session I")',
    )
    term_type: str | None = Field(
        None,
        description='Type of term (semester, academic_year, summer_session, fiscal_year, quarter, etc.)',
    )
    start_date: str | None = Field(
        None,
        description='Start date of the term (optional, for specific instances)',
    )
    end_date: str | None = Field(
        None,
        description='End date of the term (optional, for specific instances)',
    )
    description: str | None = Field(
        None,
        description='Brief description of the term or special characteristics',
    )


# ============================================================================
# ROLES & ORGANIZATIONS
# ============================================================================


from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional

class Role(BaseModel):
    """A Role represents a functional position or responsibility in the BU Housing Organization context.
    
    CCO Alignment: cco:Role - A realizable entity realized by a person in virtue of some process
    BU Context: Aligned with BU's "Affiliation" concept (student, employee, faculty, affiliate, alumni)
    Domain Context: Housing-related roles without storing PII
    Privacy Design: This entity type stores NO PII (no names, IDs, contact info).
    Instead, it captures the role, responsibilities, and organizational context.
    
    KG RELATIONSHIP PATTERNS FOR ROLES:
    - (:Role)-[:AUTHORS]->(:Procedure)
    - (:Role)-[:APPROVED]->(:Procedure)
    - (:Role)-[:FOLLOWS]->(:Procedure)
    - (:Role)-[:SUPERVISES]->(:Role)
    
    CONDITIONAL FIELD LOGIC:
    - When affiliation_type is 'employee': job_title, department, and responsibilities are expected
    - When affiliation_type is 'student': student_role is expected
    """
    
    affiliation_type: Literal["employee", "student", "faculty", "affiliate", "alumni"] = Field(
        ...,
        description="BU Affiliation type"
    )
    
    # Employee-specific fields
    job_title: Optional[str] = Field(
        None,
        description="Job title or position (required for employees)"
    )
    department: Optional[str] = Field(
        None,
        description="Department or organizational unit (required for employees)"
    )
    responsibilities: Optional[str] = Field(
        None,
        description="Key responsibilities or scope of the role"
    )
    
    # Student-specific fields
    student_role: Optional[str] = Field(
        None,
        description="Student's role relative to Housing organization (resident, RA, student_worker, assignments_assistant, resServices_assistant, mailRoom_assistant)"
    )
    

    @model_validator(mode='after')
    def validate_conditional_fields(self):
        if self.affiliation_type == "employee":
            if not self.job_title:
                raise ValueError("job_title is required when affiliation_type is 'employee'")
            if not self.department:
                raise ValueError("department is required when affiliation_type is 'employee'")
        
        if self.affiliation_type == "student":
            if not self.student_role:
                raise ValueError("student_role is required when affiliation_type is 'student'")
        
        return self


# ============================================================================
# HOUSING SPATIAL HIERARCHY (5 LEVELS)
# ============================================================================
#
# KG NOTE: The spatial hierarchy should be primarily expressed through relationships:
# (:LocationArea)-[:CONTAINS]->(:Facility)-[:CONTAINS]->(:FloorOrSuite)-[:CONTAINS]->(:Room)-[:CONTAINS]->(:RoomSpace)
# and it's inverse
# (:RoomSpace)-[:LOCATED_IN]->(:Room)-[:LOCATED_IN]->(:FloorOrSuite)-[:LOCATED_IN]->(:Facility)-[:LOCATED_IN]->(:LocationArea)
#
# The parent fields (building_name, floor_or_suite, location_area) provide convenience
# for extraction, but canonical hierarchy comes from graph relationships.
# ============================================================================


class LocationArea(BaseModel):
    """A LocationArea represents a top-level geographic, campus housing area, or community.

    CCO Alignment: cco:Site - A geographic region designated for a particular purpose
    Domain Context: High-level housing area grouping (Student Village, Bay State Road Apartments, West Campus, etc.)

    Hierarchy Level: 1 of 5 (LocationArea → Building → Floor/Suite → Room → Room Space)
    
    KG RELATIONSHIP PATTERNS:
    - (:LocationArea)-[:CONTAINS]->(:Building) - Buildings in this area
    - (:LocationArea)-[:ADJACENT_TO]->(:LocationArea) - Neighboring areas
    - (:LocationArea)-[:SERVED_BY]->(:AmenityFacility) - Area-wide amenities

    Instructions for identifying and extracting location areas:
    1. Identify named campus housing areas or neighborhoods
    2. Examples: "Student Village", "Bay State Road Apartments", "West Campus", "South Campus"
    3. Note geographic boundaries or campus location
    4. Capture distinguishing characteristics of the area
    5. Track area-wide amenities (but prefer relationships to AmenityFacility entities)
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
        description='Geographic location on campus (East Campus, West Campus, Central Campus, South Campus, Fenway, Medical Campus, etc.)',
    )
    description: str | None = Field(
        None,
        description='Description of the area and its characteristics',
    )


class Building(BaseModel):
    """A Building (Facility) represents an individual building on the BU Campus, be that a residence hall, an administrative building or an academic building.

    CCO Alignment: cco:Facility - A Site that has been designed to support some particular Processual Entity
    Domain Context: Individual building within a location area (e.g., "10 Buick Street", "Kilachand Hall", "Warren Towers")

    Hierarchy Level: 2 of 5 (LocationArea → Building → Floor/Suite → Room → Room Space)
    
    KG RELATIONSHIP PATTERNS:
    - (:Building)-[:LOCATED_IN]->(:LocationArea) - Parent area
    - (:Building)-[:CONTAINS]->(:FloorOrSuite) - Floors/suites in building
    - (:Event)-[:LOCATED_AT]->(:Building) - Events in building

    Instructions for identifying and extracting buildings:
    1. Identify specific building names or addresses (e.g., "10 Buick Street", "Kilachand Hall")
    2. Extract building street address when available
    3. Note building type (traditional dorm, apartment-style, brownstone, tower, mix)
    4. Capture total capacity or number of floors
    5. Identify building-specific amenities (lobby, elevators, dining hall, laundry)
    6. Track accessibility features (ADA accessible, elevator access)
    7. Note parent location area (but prefer relationships)
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
    building_type: str | None = Field(
        None,
        description='Type of building (residence hall, administrative, academic, dining, mix use)',
    )
    total_capacity: int | None = Field(
        None,
        ge=0,  # Must be non-negative
        description='IF Residence Hall: Total number of residents the building can house',
    )
    number_of_floors: int | None = Field(
        None,
        ge=1,  # At least 1 floor
        description='Number of floors in the building',
    )
    special_designation: str | None = Field(
        None,
        description='Special building designation (honors housing, LLC, themed community, etc.)',
    )
    year_built: str | None = Field(
        None,
        description='Year the building was constructed or last renovated',
    )

    @model_validator(mode='after')
    def validate_residential_fields(self):
        residential_types = {"residence_hall", "apartment_style", "brownstone", "tower"}
        is_residential = self.building_type in residential_types
        
        # Warn (or enforce) if residential fields on non-residential building
        if not is_residential:
            if self.total_capacity is not None:
                raise ValueError("total_capacity should only be set for residential buildings")
        
        return self

class FloorOrSuite(BaseModel):
    """A FloorOrSuite represents a floor level or suite subdivision within a building.

    CCO Alignment: cco:Facility - A subdivision of a building designed to organize living spaces
    Domain Context: Floor or suite within a building (e.g., "10 Buick-0101", "Floor 3", "Suite A")

    Hierarchy Level: 3 of 5 (LocationArea → Building → Floor/Suite → Room → Room Space)
    
    KG RELATIONSHIP PATTERNS:
    - (:FloorOrSuite)-[:LOCATED_IN]->(:Building) - Parent building
    - (:FloorOrSuite)-[:CONTAINS]->(:Room) - Rooms on floor/in suite

    Instructions for identifying and extracting floors or suites:
    1. Identify floor numbers or suite identifiers (e.g., "10 Buick-0101", "Floor 3", "Suite A")
    2. Note parent building (but prefer relationships)
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
        description='Parent building name (PREFER: use [:LOCATED_IN] relationship)',
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
    
    KG RELATIONSHIP PATTERNS:
    - (:Room)-[:LOCATED_IN]->(:FloorOrSuite) - Parent floor/suite
    - (:Room)-[:CONTAINS]->(:RoomSpace) - Bed spaces in room

    Instructions for identifying and extracting rooms:
    1. Identify room numbers (e.g., "Room 101", "10 Buick-0101-A")
    2. Note parent floor/suite and building (but prefer relationships)
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
        description='Parent floor or suite identifier (PREFER: use [:LOCATED_IN] relationship)',
    )
    building_name: str = Field(
        ...,
        description='Parent building name (PREFER: use [:LOCATED_IN] relationship)',
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
    
    KG RELATIONSHIP PATTERNS:
    - (:RoomSpace)-[:LOCATED_IN]->(:Room) - Parent room
    - (:RoomSpace)-[:ADJACENT_TO]->(:RoomSpace) - Neighboring bed spaces

    Instructions for identifying and extracting room spaces:
    1. Identify bed space designators (e.g., "101A", "101B", "Bed 1", "Space A")
    2. Note parent room, floor/suite, and building (but prefer relationships)
    3. Capture space-specific features (window access, desk location, closet access)
    4. Note furniture configuration for this space
    5. Include any accessibility accommodations for this specific space
    6. Track space status (occupied, vacant, reserved)
    7. Identify special accommodations (medical, accessibility, DSA approved)
    """

    space_identifier: str = Field(
        ...,
        description='Space identifier within room (e.g., "101A", "101B", "Bed 1", "Space A")',
    )
    room_number: str = Field(
        ...,
        description='Parent room number (PREFER: use [:LOCATED_IN] relationship)',
    )
    floor_or_suite: str = Field(
        ...,
        description='Parent floor or suite identifier (PREFER: use [:LOCATED_IN] relationship)',
    )
    building_name: str = Field(
        ...,
        description='Parent building name (PREFER: use [:LOCATED_IN] relationship)',
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



# ============================================================================
# TECHNICAL ENTITIES
# ============================================================================




# ============================================================================
# ENTITY TYPE REGISTRY
# ============================================================================

# Import default entity types to include alongside BU Housing types
from models.entity_types import (
    Procedure,
    Organization,
    Event,
    Document,
    Preference,
    Requirement,
)

# Registry of all BU Housing entity types (CCO-aligned, PII-free)
# Organized by hierarchy level and function
# Includes both custom BU Housing types and relevant default Graphiti types
BU_HOUSING_ENTITY_TYPES: dict[str, type[BaseModel]] = {
    # ===== ROLES & PEOPLE (PII-free) =====
    'Role': Role,  # BU Affiliations and functional roles
    
    # ===== TEMPORAL =====
    'Term': Term,  # Academic terms, fiscal periods, time intervals

    # ===== SPATIAL HIERARCHY (5 levels) =====
    'LocationArea': LocationArea,  # Level 1: Campus housing areas (Student Village, Bay State Road)
    'Building': Building,  # Level 2: Buildings (10 Buick Street, Kilachand Hall)
    'FloorOrSuite': FloorOrSuite,  # Level 3: Floors or suites (10 Buick-0101, Floor 3)
    'Room': Room,  # Level 4: Individual rooms (Room 101, 10 Buick-0101-A)
    'RoomSpace': RoomSpace,  # Level 5: Bed spaces (101A, 101B, Bed 1)

    # ===== DEFAULT GRAPHITI TYPES (for general-purpose entities) =====
    'Procedure': Procedure,  # Standard operating procedures
    'Organization': Organization,  # Companies, institutions, departments
    'Event': Event,  # Time-bound activities and occurrences
    'Document': Document,  # Information content (reports, articles, etc.)
    'Preference': Preference,  # User preferences and choices
    'Requirement': Requirement,  # Specific needs or specifications
}
