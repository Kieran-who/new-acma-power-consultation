import weaviate.classes as wvc

weav_classes = {
    "classes": [
        {
            "class": "Submission",
            "description": "Submission Document",
            "vectorizer_config": wvc.config.Configure.Vectorizer.none(),
            "properties": [
                wvc.config.Property(
                    data_type=wvc.config.DataType.TEXT,
                    name="author",                    
                    description="The author of the submission",
                    skip_vectorization=True,
                ),
                wvc.config.Property(
                    name="substantive_submission",
                    data_type=wvc.config.DataType.BOOL,
                    description="Does the submission provide a substantive response to the consultation",
                    skip_vectorization=True,
                ),                
                wvc.config.Property(
                    name="responder_category",
                    data_type=wvc.config.DataType.TEXT,
                    description="Category of the responder",
                    skip_vectorization=True,
                ),
                wvc.config.Property(
                    name="support",
                    data_type=wvc.config.DataType.TEXT,
                    description="Does the responder support the consultation",
                    skip_vectorization=True,
                ),                 
                 wvc.config.Property(
                    name="motivations",
                    data_type=wvc.config.DataType.TEXT_ARRAY,
                    description= "Top 3 motivations for the submission.",
                    skip_vectorization=True,
                 ),
                 wvc.config.Property(
                    name="regulation",
                    data_type=wvc.config.DataType.TEXT,
                    description= "Does this submission make any comment on the form of regulation provided?",
                    skip_vectorization=True,
                 ),
                 wvc.config.Property(
                    name="perceived_impact",
                    data_type=wvc.config.DataType.TEXT,
                    description= "How does the submitter perceive the impact of the proposed laws?",
                    skip_vectorization=True,
                 ),
                 wvc.config.Property(
                    name="regulator_trust",
                    data_type=wvc.config.DataType.TEXT,
                    description= "Does the submission express trust or skepticism towards the ACMA's ability?",
                    skip_vectorization=True,
                 ),
                 wvc.config.Property(
                    name="changes",
                    data_type=wvc.config.DataType.TEXT,
                    description= "Changes the submitter would like to see in the proposed laws.",
                    skip_vectorization=True,
                 ),
                 wvc.config.Property(
                    name="file_name",
                    data_type=wvc.config.DataType.TEXT,
                    description= "The name of the submission file",
                    skip_vectorization=True,
                 ),                 
                 wvc.config.Property(
                    name="definitions",
                    data_type=wvc.config.DataType.TEXT,
                    description= "thoughts on definitions",
                    skip_vectorization=True,
                 ),
                 wvc.config.Property(
                    name="questions",
                    data_type=wvc.config.DataType.TEXT,
                    description= "The responses to specific questions for type.",
                    skip_vectorization=True,
                 )
            ]
        },        
    ]
}
